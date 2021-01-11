from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil
import logger

dbAPI = Database()
logger.info("Starting tw following")
for project in dbAPI.get_projects():
    
    try:
        account = dbAPI.get_next_tw_user_to_follow(project.project_id)
        if account:
            tw_util = TwitterUtil(project.twitter_config)
            tw_util.follow(account.user_id)
            dbAPI.record_tw_follow(account)
    except Exception as e:
        logger.error(e)

logger.info("Tw follower finished")