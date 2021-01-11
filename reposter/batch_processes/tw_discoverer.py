from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil
import logger

dbAPI = Database()
logger.info("Starting tw discovering")
for project in dbAPI.get_projects():
    if dbAPI.no_more_tw_accounts_to_follow(project.project_id):
        try:
            eng = dbAPI.get_next_tw_engagement_account(project.project_id)
            if eng:    
                tw_util = TwitterUtil(project.twitter_config)
                result = tw_util.get_followers_of(eng.username, eng.cursor)
                eng.cursor = result["cursor"]
                dbAPI.update_tw_cursor(eng)
                dbAPI.add_tw_followers(result["followers"], eng.eng_id)
        except Exception as e:
            logger.error(e)

logger.info("Tw discovering finished")
