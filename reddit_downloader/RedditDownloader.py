import praw
import requests
import os
import json
import concurrent.futures
import re
import youtube_dl
from media_util import is_an_image

class RedditDownloader:
    def __init__(self, 
                 config, 
                 post_exists, 
                 record_post,
                 number = 10):
        self.subreddit = config["subreddit"]
        self.filter = config["filter"]
        self.path = config["path"]
        self.reddit = praw.Reddit(client_id = config["client_id"],
                                  client_secret = config["client_secret"],
                                  user_agent = "pabloi09.reddit.downloader")
        self.posts = []
        self.number = number
        self.post_exists = post_exists
        self.record_post = record_post
        self.downloaded = []

    
    def start(self):
        try:
            submissions = self.get_submissions_by_filter()
            self.get_posts_info(submissions)
            if len(self.posts) > 0:
                self.run_concurrent_download()
                #self.run_linear_download()
                for post_id in self.downloaded:
                    self.record_post(post_id)
        except Exception as e:
            print(e)
    
    def get_submissions_by_filter(self):
        if self.filter == 'hot':
            return self.reddit.subreddit(self.subreddit).hot(limit=None)
        elif self.filter == 'top':
            return self.reddit.subreddit(self.subreddit).top(limit=None)
        elif self.filter == 'new':
            return self.reddit.subreddit(self.subreddit).new(limit=None)
    
    def get_posts_info(self, submissions):
        for submission in submissions:
            post = {}
            if submission.stickied:
                continue
            if is_an_image(submission.url):
                post = self.get_image_post_data(post,submission)
            elif self.is_a_video(submission):
                post = self.get_video_post_data(post, submission)
            if post:
                self.add_post_or_continue(post)
            if len(self.posts) >= self.number:
                break

    def run_concurrent_download(self):
        if self.path_does_not_exist():
            os.makedirs(self.path)
        with concurrent.futures.ThreadPoolExecutor() as ptolemy:
            ptolemy.map(self.download_post, self.posts)
    
    def run_linear_download(self): #testing purposes
        if self.path_does_not_exist():
            os.makedirs(self.path)
        for post in self.posts:
            self.download_post(post)

    def is_a_video(self, submission):
        return submission.media
    
    def get_image_post_data(self, post, submission):
        post = self.get_post_data(post, submission)
        return post
    
    def get_video_post_data(self, post, submission):
        post = self.get_post_data(post, submission)
        post["fname"] = post["fname"] + ".mp4"
        url = submission.media['reddit_video']['fallback_url']
        post["source_url"]  = url.split("?")[0]
        return post
    
    def get_post_data(self, post, submission):
        post["id"] = re.search('(?s:.*)\w/(.*)', submission.url).group(1).split(".")[0]
        post["dir"] = self.path + post["id"] + "/" 
        post["fname"]= post["dir"] + re.search('(?s:.*)\w/(.*)', submission.url).group(1)
        post["post_url"] = "redd.it/" + submission.id
        post["source_url"] = submission.url
        post["url"] = submission.url
        post["author"] = submission.author.name
        post["title"] = submission.title
        return post

    def add_post_or_continue(self, post):
        if not self.post_exists(post["id"]):
            self.posts.append(post)
    
    def path_does_not_exist(self):
        return not os.path.exists(self.path)

    def download_post(self, post):
        try:
            os.makedirs(post["dir"])
            if is_an_image(post["fname"]):
                self.download_and_save_image(post)
            else:
                self.download_and_save_video(post)
            
            self.save_metadata(post)
            self.downloaded.append(post["id"])
        except Exception as e:
            print(e)
            
    
    def download_and_save_image(self,post):
        r = requests.get(post["source_url"])
        with open(post["fname"], "wb") as f:
            f.write(r.content)
    
    def download_and_save_video(self,post):
        ydl_opts = {"outtmpl": post["fname"]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post["source_url"]])

    def save_metadata(self, post):
        metadata = {"author" : post["author"],
                    "post_url" : post["post_url"],
                    "title": post["title"]}
        met_file = post["dir"] + re.search('(?s:.*)\w/(.*)', post["url"]).group(1).split(".")[0] + ".json"
        with open(met_file, "w") as f:
            json.dump(metadata, f)
    


    



