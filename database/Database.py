from database.create_tables import create_tables
from database.create_test_data import create_test_data
import os
from database.model import User, Project, TwitterAccountToFollow, Post, InstaAccountToFollow
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
    
    def record_post(self, post_id, project_id):
        self.connect()
        self.cursor.execute("insert into post(post_id, project_id) values (?,?)", (post_id, project_id))
        self.disconnect()

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
        posts = self.cursor.fetchall()
        self.disconnect()
        return [Post.from_database(post) for post in posts]
    
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
    