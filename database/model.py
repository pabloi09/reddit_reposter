import sqlite3
import json
from database.Security import Security

class User:
    def __init__(self, username, password, salt = None):
        self.username = username
        self.password, self.salt = Security.encrypt_password(password, salt)

    def to_insert(self):
        return (self.username, self.password, self.salt)

    @classmethod
    def from_database(cls, row):
        return cls(row["user_id"], row["username"])


class Project:
    def __init__(self, reddit_config, twitter_config, insta_config, user_id, s = None):
        self.s = Security() if s is None else s
        self.reddit_config, self.twitter_config, self.insta_config, self.user_id = reddit_config, twitter_config, insta_config, user_id
    
    def to_insert(self):
        reddit_config = self.s.cipher(json.dumps(self.reddit_config))
        twitter_config = self.s.cipher(json.dumps(self.twitter_config))
        insta_config = self.s.cipher(json.dumps(self.insta_config))
        return (reddit_config, twitter_config, insta_config, self.user_id)

    @classmethod
    def from_database(cls, row):
        s = Security()
        reddit_config = json.loads(s.decipher(row["reddit_config"]))
        twitter_config = json.loads(s.decipher(row["twitter_config"]))
        insta_config = json.loads(s.decipher(row["insta_config"]))
        result = cls(reddit_config, twitter_config, insta_config, row["user_id"], s)
        result.project_id = row["project_id"]
        return result
    

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

