import tweepy
import os
import json
import time
import VideoMedia

class TwitterBot:
    def __init__(self, config):
        auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
        auth.set_access_token(config["access_token"], config["access_token_secret"])
        self.api = tweepy.API(auth)
        self.auth = auth.apply_auth()
    
    def test_tweet(self, post):
        self.api.update_status(post)

    def tweet_post(self, path, template):
        filename, metadata = self.get_post_data(path)
        
        if self.is_a_video(filename):
            media = VideoMedia.VideoMedia(filename, self.auth)
            media.upload_video()
        else:
            media = self.api.media_upload(filename)

        status = template.format(metadata["title"], metadata["author"] ,metadata["post_url"])
        self.api.update_status(status=status, media_ids=[media.media_id])
    
    def get_post_data(self, path):
        filename = ""
        metadata = {}
        for temp_filename  in os.listdir(path):
            temp_filename = path + temp_filename 
            if os.path.isfile(temp_filename):
                if self.is_metadata_file(temp_filename):
                    metadata = self.get_metadata()
                else:
                    filename = temp_filename
        return filename, metadata
                    
    
    def is_metadata_file(self, filename):
        return filename.endswith(".json")
    
    def get_metadata(self, filename):
        with open(temp_filename) as metadata_json:
            metadata = json.load(metadata_json)
        return metadata
    
    def is_a_video(self,filename):
        return filename.endswith(".mp4")





