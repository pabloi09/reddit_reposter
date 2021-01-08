from database.model import User, Project, TwitterAccountToFollow, Post, InstaAccountToFollow
import sqlite3
import json

REDDIT_PATH = "/var/www/html/data/{}/reddit/{}/"
INSTA_PATH = "/var/www/html/data/{}/insta/{}/"
PROJECT_PATH = "/reposter/{}"
#PROJECT_PATH = "/home/pablo/projects/reddit_reposter/reposter/{}"
def create_test_data(file):
    
    conn = sqlite3.connect(file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    users = [
        User("pabloi09","password").to_insert(),
        User("prueba","password").to_insert(),
        User("prueba2","password").to_insert(),
    ]

    with open(PROJECT_PATH.format("reddit_downloader/config.json")) as json_config:
        reddit_config = json.load(json_config)

    with open(PROJECT_PATH.format("twitter_util/config.json")) as json_config:
        twitter_config = json.load(json_config)
    
    with open(PROJECT_PATH.format("instagram_util/config.json")) as json_config:
        insta_config = json.load(json_config)

    projects = [
        Project(reddit_config, twitter_config, insta_config,1).to_insert(),
        #Project(reddit_config, twitter_config, insta_config,1).to_insert(),
        #Project(reddit_config, twitter_config, insta_config,2).to_insert(),
        #Project(reddit_config, twitter_config, insta_config,3).to_insert(),
        #Project(reddit_config, twitter_config, insta_config,3).to_insert(),
        ]
    
    cursor.executemany("INSERT INTO project(reddit_config, twitter_config, insta_config, user_id) VALUES (?,?,?,?)", projects)
    conn.commit()
    cursor.execute("select * from project")
    projects = cursor.fetchall()
    for project in projects:
        p = Project.from_database(project)
        p.reddit_config["path"] = REDDIT_PATH.format(p.user_id, p.project_id)
        p.insta_config["cookie_location"] = INSTA_PATH.format(p.user_id, p.project_id)
        q = p.to_insert()
        cursor.execute("UPDATE project SET reddit_config = ?, insta_config = ? WHERE project_id = ?", (q[0],q[2],p.project_id))    
        cursor.executemany("INSERT INTO tw_engagement(username, project_id) VALUES (?,?)", [(username, p.project_id) for username in twitter_config["engagement_accounts"]])
        cursor.executemany("INSERT INTO insta_engagement(username, project_id) VALUES (?,?)", [(username, p.project_id) for username in insta_config["engagement_accounts"]])
        conn.commit()
    
    conn.close()

