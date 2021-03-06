from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil


dbAPI = Database()

for project in dbAPI.get_projects():
    
    try:
        account = dbAPI.get_next_tw_user_to_follow(project.project_id)
        tw_util = TwitterUtil(project.twitter_config)
        tw_util.follow(account.user_id)
        dbAPI.record_tw_follow(account)
    except Exception as e:
        print(e)