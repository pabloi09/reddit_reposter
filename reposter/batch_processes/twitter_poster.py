from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil
import logger

PATH_TEMPLATE = "{}{}/"

dbAPI = Database()
logger.info("Starting tw poster")
for project in dbAPI.get_projects():
    
    try:
        post = dbAPI.get_next_tw_post(project.project_id)
        if post:
            tw_util = TwitterUtil(project.twitter_config)
            path = PATH_TEMPLATE.format(project.reddit_config["path"], post.post_id )
            tw_util.tweet_post(path)
            dbAPI.record_upload_tw(post.post_id, project.project_id)
    except Exception as e:
        logger.error(e)

logger.info("Tw poster finished")
    

