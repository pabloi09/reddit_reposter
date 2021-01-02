import TwitterUtil
import json

if __name__ == '__main__':
    with open("config.json") as json_config:
        config = json.load(json_config)
    
    bot = TwitterUtil.TwitterUtil(config)
    #bot.tweet_post("/path/to/filedir")
    #bot.test_tweet("Is the token working?")
    bot.follow("@davidbroncano")