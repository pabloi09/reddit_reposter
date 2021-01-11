from database.Database import Database
from reddit_downloader.RedditDownloader import RedditDownloader
import logger

dbAPI = Database()

    
for project in dbAPI.get_projects():

    def post_exists(post_id):
        return dbAPI.post_exists(post_id, project.project_id)
    
    def record_post(post_id):
        dbAPI.record_post(post_id, project.project_id)
    
    logger.info("Starting download job")
    downloader = RedditDownloader(project.reddit_config, 
                                  post_exists, 
                                  record_post, 
                                  number=20)
    downloader.start()
    logger.info("Download job finished")