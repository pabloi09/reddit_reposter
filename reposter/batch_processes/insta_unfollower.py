from database.Database import Database
from instagram_util.InstaUtil import InstaUtil
import logger

dbAPI = Database()
logger.info("Starting insta unfollowing")
for project in dbAPI.get_projects():
    account = None
    try:
        account = dbAPI.get_next_insta_user_to_unfollow(project.project_id, days = 1)
        if account:
            insta_util = InstaUtil(project.insta_config)
            insta_util.unfollow(account.user_id)
    except Exception as e:
        logger.error(e)
    finally:
        if account is not None:
            dbAPI.record_insta_unfollow(account)

logger.info("Insta unfollowing finished")