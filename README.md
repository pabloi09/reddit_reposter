# Reddit reposter
The project idea is to create a whole framework to repost posts of a subreddit in both twitter and instagram accounts. This framework will also have the ability
to engage new followers with following techniques.

- [x] Core framework : bots, database and related tools
- [ ] API Restful : api to communcate a web application with the core framework
- [ ] Web application : for other users to create accounts and use this framework

# Try it now
The core framework is done and can be installed and used right now

## 1. Install docker 

The instructions can be found <a href="https://docs.docker.com/engine/install/ubuntu/">here</a>

## 2. Download this project
```
git clone https://github.com/pabloi09/reddit_reposter.git
cd reddit_reposter
```

## 3. Configure your developer options in the three social media web pages:
- **For Twitter:** create a new app inside a new Project with read/write permissions from the <a href = "https://developer.twitter.com"> Developer Portal </a>
- **For Reddit:**  create a new application from the <a href="https://www.reddit.com/prefs/apps/">Preferences</a>
- **For Instagram:** it is advised to make the account a Business account

## 4. Edit the three config.json files with the required keys obtained in the previous step 
- reposter/instagram_util/config.json
- reposter/reddit_downloader/config.json
- reposter/twitter_util/config.json

## 5. Start the container
```
chmod +x start.sh
./start.sh
```

The routines are preconfigured. You can always change the behavior taking a look to the code :sunglasses:
