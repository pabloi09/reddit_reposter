from database.Database import Database
import shutil

PATH_TEMPLATE = "{}{}"

dbAPI = Database("db.db")

for project in dbAPI.get_projects():
    
    posts = dbAPI.get_finished_posts(project.project_id)

    for post in posts:
        try:
            path = PATH_TEMPLATE.format(project.reddit_config["path"], post.post_id)
            shutil.rmtree(path)
            dbAPI.record_closed_post(post.post_id, project.project_id)
        except Exception as e:
            print(e)
    