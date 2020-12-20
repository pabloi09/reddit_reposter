import sqlite3
import json
from Security import Security

class User:
    def __init__(self, user_id, username, password, salt = None):
        self.user_id, self.username = user_id, username
        self.password, self.salt = Security.encrypt_password(password, salt)

    def to_insert(self):
        return (self.user_id, self.username, self.password, self.salt)

    @classmethod
    def from_database(cls, row):
        return cls(row["user_id"], row["username"])


class Project:
    def __init__(self, project_id, reddit_config, twitter_config, insta_config):
        self.s = Security()
        self.project_id, self.reddit_config, self.twitter_config, self.insta_config = project_id, reddit_config, twitter_config, insta_config
    
    def to_insert(self):
        reddit_config = self.s.cipher(json.dump(self.reddit_config))
        twitter_config = self.s.cipher(json.dump(self.twitter_config))
        insta_config = self.s.cipher(json.dump(self.insta_config))
        return (self.project_id, reddit_config, twitter_config, insta_config)

    @classmethod
    def from_database(cls, row):
        reddit_config = json.load(self.s.decipher(row["reddit_config"]))
        twitter_config = json.load(self.s.decipher(row["twitter_config"]))
        insta_config = json.load(self.s.decipher(row["insta_config"]))
        return cls(row["project_id"], row["reddit_config"], row["twitter_config"], row["insta_config"])
    
class TwitterAccountToFollow:
    def __init__(self, user_id, date_follow, date_unfollow):
        self.user_id, self.date_follow, self.date_unfollow = user_id, date_follow, date_unfollow

    def to_insert(self):
        return (self.user_id, self.date_follow, self.date_unfollow)

    @classmethod
    def from_database(cls, row):
        return cls(row["user_id"], row["date_follow"], row["date_unfollow"])
    
class Post:
    def __init__(self, post_id, date_uploaded_tw, date_uploaded_insta):
        self.post_id, self.date_uploaded_tw, self.date_uploaded_insta = post_id, date_uploaded_tw,date_uploaded_insta
    
    def to_insert(self):
        return (self.post_id, self.date_uploaded_tw, self.date_uploaded_insta)
    
    @classmethod
    def from_database(cls, row):
        return cls(row["post_id"], row["date_uploaded_tw"], row["date_uploaded_insta"])
    
class InstaAccountToFollow:
    def __init__(self, user_id, date_follow, date_unfollow):
        self.user_id, self.date_follow, self.date_unfollow = user_id, date_follow, date_unfollow

    def to_insert(self):
        return (self.user_id, self.date_follow, self.date_unfollow)

    @classmethod
    def from_database(cls, row):
        return cls(row["user_id"], row["date_follow"], row["date_unfollow"])

