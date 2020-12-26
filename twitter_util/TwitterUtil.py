import tweepy
import os
import json
import time
import VideoMedia
from media_util import is_a_video, get_post_data

class TwitterUtil:
    def __init__(self, config):
        auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
        auth.set_access_token(config["access_token"], config["access_token_secret"])
        self.api = tweepy.API(auth)
        self.auth = auth.apply_auth()
    
    def test_tweet(self, post):
        self.api.update_status(post)

    def tweet_post(self, path, template):
        filename, metadata = get_post_data(path)
        
        if is_a_video(filename):
            media = VideoMedia.VideoMedia(filename, self.auth)
            media.upload_video()
        else:
            media = self.api.media_upload(filename)

        status = template.format(metadata["title"], metadata["author"] ,metadata["post_url"])
        self.api.update_status(status=status, media_ids=[media.media_id])
    
    def get_followers_of(self, user, cursor): #1 lista/h
        followers, cursor = self.api.followers_ids(screen_name=user,cursor=cursor)
        result = {"followers": followers, "cursor": cursor}
        return result
    
    def follow(self, user_id): #1 follow/ 3 min y 45 segundos Max num de seguidos: 400/dia 5000 en total. Hacer unfollows cada 13 días como máximo. Se va a hacer por semana
        self.api.create_friendship(user_id)
    
    def unfollow(self, user_id):
        self.api.destroy_friendship(user_id)
    
    def check_if_follows_me(self, user_id):
        friendship = self.api.show_friendship(user_id)






