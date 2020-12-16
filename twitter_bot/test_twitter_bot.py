import TwitterBot
import json

if __name__ == '__main__':
    with open("config.json") as json_config:
        config = json.load(json_config)
    
    bot = TwitterBot.TwitterBot(config)
    bot.tweet_post("/path/to/filedir", "{} \nby {} via {}")
    #bot.test_tweet("Is the token working?")