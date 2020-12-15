import tweepy

class TwitterBot:
    def __init__(self, config):
        auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
        auth.set_access_token(config["access_token"], config["access_token_secret"])
        self.api = tweepy.API(auth)
    
    def test_tweet(self, post):
        self.api.update_status(post)



