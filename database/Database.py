from database.create_tables import create_tables
from database.create_test_data import create_test_data
import os
from database.model import User, Project, TwitterAccountToFollow, Post, InstaAccountToFollow
import sqlite3

class Database:
    def __init__(self, file):
        if not os.path.isfile(file):
            create_tables(file)
            create_test_data(file)
        self.file = file
    
    def connect(self):
        self.connection = sqlite3.connect(self.file)
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
    