from database.Database import Database
from instagram_util.InstaUtil import InstaUtil
import logger
dbAPI = Database()

logger.info("Starting insta following")
for project in dbAPI.get_projects():
    
    try:
        account = dbAPI.get_next_insta_user_to_follow(project.project_id)
        if account:
            insta_util = InstaUtil(project.insta_config)
            insta_util.follow(account.user_id)
            dbAPI.record_insta_follow(account)
    except Exception as e:
        logger.error(e)
    
logger.info("Insta following finished")