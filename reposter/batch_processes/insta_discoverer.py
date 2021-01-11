from database.Database import Database
from instagram_util.InstaUtil import InstaUtil
import logger

dbAPI = Database()
logger.info("Starting insta discovering")
for project in dbAPI.get_projects():
    if dbAPI.no_more_insta_accounts_to_follow(project.project_id):
        try:
            eng = dbAPI.get_next_insta_engagement_account(project.project_id)
            if eng:
                insta_util = InstaUtil(project.insta_config)
                followers, cursor = insta_util.get_followers_of(eng.username, eng.cursor)
                eng.cursor = cursor
                dbAPI.update_insta_cursor(eng)
                dbAPI.add_insta_followers(followers, eng.eng_id)
        except Exception as e:
            logger.error(e)

logger.info("Insta discovering finished")