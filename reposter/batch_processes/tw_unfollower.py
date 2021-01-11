from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil
import logger

dbAPI = Database()
logger.info("Starting tw unfollowing")
for project in dbAPI.get_projects():
    account = None
    try:
        account = dbAPI.get_next_tw_user_to_unfollow(project.project_id, days = 1)
        if account:
            tw_util = TwitterUtil(project.twitter_config)
            tw_util.unfollow(account.user_id)
    except Exception as e:
        logger.error(e)
    finally:
        if account is not None:
            dbAPI.record_tw_unfollow(account)

logger.info("Tw unfollowing finished")