from database.Database import Database
from reddit_downloader.RedditDownloader import RedditDownloader

dbAPI = Database()

    
for project in dbAPI.get_projects():

    def post_exists(post_id):
        return dbAPI.post_exists(post_id, project.project_id)
    
    def record_post(post_id):
        dbAPI.record_post(post_id, project.project_id)
    
    downloader = RedditDownloader(project.reddit_config, 
                                  post_exists, 
                                  record_post, 
                                  number=10)
    downloader.start()