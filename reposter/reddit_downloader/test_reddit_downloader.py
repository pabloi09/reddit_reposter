import json
import RedditDownloader

if __name__ == '__main__':
    with open("config.json") as json_config:
        config = json.load(json_config)
    downloader = RedditDownloader.RedditDownloader(config)
    downloader.start()