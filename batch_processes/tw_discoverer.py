from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil

dbAPI = Database("db.db")

for project in dbAPI.get_projects():
    tw_util = TwitterUtil(project.twitter_config)
    eng = dbAPI.get_next_tw_engagement_account(project.project_id)

    try:
        result = tw_util.get_followers_of(eng.username, eng.cursor)
        eng.cursor = result["cursor"]
        dbAPI.update_tw_cursor(eng)
        dbAPI.add_tw_followers(result["followers"], eng.eng_id)
    except Exception as e:
        print(e)
