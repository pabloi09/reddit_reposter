from database.Database import Database
import shutil
import os
from datetime import datetime
import logger

PATH_TEMPLATE = "{}{}"

dbAPI = Database()
logger.info("Starting file cleaning")
for project in dbAPI.get_projects():
    
    posts = dbAPI.get_finished_posts(project.project_id)

    for post in posts:
        try:
            path = PATH_TEMPLATE.format(project.reddit_config["path"], post.post_id)
            shutil.rmtree(path)
            dbAPI.record_closed_post(post.post_id, project.project_id)
            now = datetime.now()
            yesterday = now - datetime.timedelta(days = 1)
            os.system("mv /reposter/batch.log /reposter/batch.log.{}".format(yesterday.strftime('%Y-%m-%d')))
            last_week = now - datetime.timedelta(days = 7)
            last_week_file  = "batch.log.{}".format(last_week.strftime('%Y-%m-%d'))
            if os.path.isfile(last_week_file):
                os.system("rm {}".format(last_week_file))
        except Exception as e:
            logger.error(e)
            
logger.info("File cleaning finished")
    