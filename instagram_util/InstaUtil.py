from instabot import Bot
from media_util import is_a_video, get_post_data, PhotoCropper
TMP_COOKIE_LOCATION = "./config"

class InstaUtil:

    def __init__(self, config):
        self.cookie_location = config["cookie_location"]
        self.bot = Bot(base_path = config["cookie_location"],
                       follow_delay = 0, 
                       unfollow_delay = 0,
                       max_follows_per_day=10000,
                       max_unfollows_per_day=10000)
        self.bot.login(username= config["username"], password= config["password"])

    def publish_post(self, path, template):
        filename, metadata = get_post_data(path)
        caption = template.format(metadata["title"], metadata["author"] ,metadata["post_url"])
        
        if is_a_video(filename):
            self.bot.upload_video(filename, caption=caption)
        else:
            PhotoCropper().prepare_and_fix_photo(filename)
            self.bot.upload_photo(filename, caption=caption)
    
    def get_followers_of(self, user_id, nfollowers = None):
        return self.bot.get_user_followers(user_id, nfollowers)
    
    def follow(self, user_id): # 200 follows/ día. 1 follow/ 7 min y 30 seg. Mejor randomizar la distribución y el número de follows al día. Entre 160 y 180 por ejemplo. Randomizadamente distribuidos
        return self.bot.follow(user_id)
    
    def unfollow(self, user_id):
        return self.bot.unfollow(user_id)
        
    
    

    

