from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil

PATH_TEMPLATE = "{}{}/"

dbAPI = Database()

for project in dbAPI.get_projects():
    
    post = dbAPI.get_next_tw_post(project.project_id)
    tw_util = TwitterUtil(project.twitter_config)
    path = PATH_TEMPLATE.format(project.reddit_config["path"], post.post_id )
    try:
        tw_util.tweet_post(path)
        dbAPI.record_upload_tw(post.post_id, project.project_id)
    except Exception as e:
        print(e)
    

