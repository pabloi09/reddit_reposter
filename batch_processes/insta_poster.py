from database.Database import Database
from instagram_util.InstaUtil import InstaUtil

PATH_TEMPLATE = "{}{}/"

dbAPI = Database("db.db")

for project in dbAPI.get_projects():
    
    post = dbAPI.get_next_insta_post(project.project_id)
    insta_util = InstaUtil(project.insta_config)
    path = PATH_TEMPLATE.format(project.reddit_config["path"], post.post_id )
    try:
        insta_util.publish_post(path)
        dbAPI.record_upload_insta(post.post_id, project.project_id)
    except Exception as e:
        print(e)
    