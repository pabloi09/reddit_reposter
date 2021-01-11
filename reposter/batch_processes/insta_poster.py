from database.Database import Database
from instagram_util.InstaUtil import InstaUtil
import logger
PATH_TEMPLATE = "{}{}/"

dbAPI = Database()
logger.info("Starting insta poster")
for project in dbAPI.get_projects():
    
    try:
        post = dbAPI.get_next_insta_post(project.project_id)
        if post:
            insta_util = InstaUtil(project.insta_config)
            path = PATH_TEMPLATE.format(project.reddit_config["path"], post.post_id )
            insta_util.publish_post(path)
            dbAPI.record_upload_insta(post.post_id, project.project_id)
    except Exception as e:
        logger.error(e)

logger.info("Insta poster finished")