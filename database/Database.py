import create_tables
import os
from model import User, Project, TwitterAccountToFollow, Post, InstaAccountToFollow

class Database:
    def __init__(self, file):
        if not os.path.isfile(file):
            create_tables(file)
    