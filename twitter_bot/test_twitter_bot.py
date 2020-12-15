import TwitterBot
import json

if __name__ == '__main__':
    with open("config.json") as json_config:
        config = json.load(json_config)
    
    bot = TwitterBot.TwitterBot(config)
    bot.test_tweet("Hello world!")
