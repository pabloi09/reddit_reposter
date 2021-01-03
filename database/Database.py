from database.create_tables import create_tables
from database.create_test_data import create_test_data
import os
from database.model import User, Project, TwitterAccountToFollow, Post, InstaAccountToFollow, TwitterEngagement
import sqlite3
import datetime

class Database:
    def __init__(self, file):
        if not os.path.isfile(file):
            create_tables(file)
            create_test_data(file)
        self.file = file
    
    def connect(self):
        self.connection = sqlite3.connect(self.file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.commit()
        self.connection.close() 
    
    #GETTERS
    
    def get_projects(self):
        self.connect()
        self.cursor.execute("select * from project")
        result = []
        for project in self.cursor:
            result.append(Project.from_database(project))
        self.disconnect()
        return result
    
    def post_exists(self, post_id, project_id):
        self.connect()
        self.cursor.execute("select * from post where post_id=? and project_id=?", (post_id,project_id))
        posts = self.cursor.fetchall()
        self.disconnect()
        return len(posts) > 0
    
    def get_next_tw_post(self, project_id):
        self.connect()
        self.cursor.execute("select * from post where closed = ? and project_id = ? and date_uploaded_tw is ?", (False, project_id, None))
        post = self.cursor.fetchone()
        self.disconnect()
        return Post.from_database(post)

    def get_next_insta_post(self, project_id):
        self.connect()
        self.cursor.execute("select * from post where closed = ? and project_id = ? and date_uploaded_tw is not ? and date_uploaded_insta is ?", (False, project_id, None, None))
        post = self.cursor.fetchone()
        self.disconnect()
        return Post.from_database(post)

    def get_finished_posts(self, project_id):
        self.connect()
        self.cursor.execute("select * from post where closed = ? and project_id = ? and date_uploaded_tw is not ? and date_uploaded_insta is not ?", (False, project_id, None, None))
        posts = [Post.from_database(post) for post in self.cursor]
        self.disconnect()
        return posts
    
    def get_next_tw_engagement_account(self, project_id):
        self.connect()
        self.cursor.execute("select * from tw_engagement where finished = ? and cursor is not ? and project_id = ?", (False, 0, project_id))
        engagement = TwitterEngagement.from_database(self.cursor.fetchone())
        self.disconnect()
        return engagement
    
    def get_next_tw_user_to_follow(self, project_id):
        self.connect()
        self.cursor.execute("""SELECT tw_followed.* from twitter_followed 
                               inner join tw_engagement 
                               on tw_engagement.eng_id = tw_followed.eng_id 
                               where tw_followed.date_follow is null 
                               and tw_engagement.project_id = ?;""",(project_id,))
        account = TwitterAccountToFollow.from_database(self.cursor.fetchone())
        self.disconnect()
        return account

    
    #SETTERS
    
    def record_post(self, post_id, project_id):
        self.connect()
        self.cursor.execute("insert into post(post_id, project_id) values (?,?)", (post_id, project_id))
        self.disconnect()
    
    def record_upload_tw(self, post_id, project_id):
        ts = datetime.datetime.now()
        self.connect()
        self.cursor.execute("update post set date_uploaded_tw = ? where post_id = ? and project_id = ?", (ts,post_id, project_id))
        self.disconnect()
    
    def record_upload_insta(self, post_id, project_id):
        ts = datetime.datetime.now()
        self.connect()
        self.cursor.execute("update post set date_uploaded_insta = ? where post_id = ? and project_id = ?", (ts,post_id, project_id))
        self.disconnect()
    
    def record_closed_post(self, post_id, project_id):
        self.connect()
        self.cursor.execute("update post set closed = ? where post_id = ? and project_id = ?", (True, post_id, project_id))
        self.disconnect()
    
    def update_tw_cursor(self, engagement):
        self.connect()
        self.cursor.execute("update tw_engagement set username = ?, cursor = ?, finished = ? where eng_id = ?", (engagement.to_insert() + (engagement.eng_id,)))
        self.disconnect()
    
    def add_tw_followers(self, followers, eng_id):
        self.connect()
        self.cursor.executemany("insert into tw_followed(user_id, eng_id) values (?,?)", [(user_id, eng_id) for user_id in followers])
        self.disconnect()
    
    def record_tw_follow(self, account):
        self.connect()
        account.date_follow = datetime.datetime.now()
        self.cursor.execute("update tw_followed set user_id = ?, date_follow = ?, date_unfollow = ? where eng_id = ? and user_id = ?", (account.to_insert() + (account.eng_id, account.user_id)))
        self.disconnect()
    
    

    
    