from InstaUtil import InstaUtil
import json
import time
from numpy import random

if __name__ == '__main__':
    with open("config.json") as json_config:
        config = json.load(json_config)
    
    bot = InstaUtil(config)
    bot.publish_post("/url/to/dir", "{} \nby {} via {}")
    followers = bot.get_followers_of("user")
    for follower in followers:
        time.sleep(random.uniform(1,3))
        bot.follow(follower)
        