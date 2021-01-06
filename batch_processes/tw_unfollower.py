from database.Database import Database
from twitter_util.TwitterUtil import TwitterUtil


dbAPI = Database("db.db")

for project in dbAPI.get_projects():
    account = None
    try:
        account = dbAPI.get_next_tw_user_to_unfollow(project.project_id)
        tw_util = TwitterUtil(project.twitter_config)
        tw_util.unfollow(account.user_id)
    except Exception as e:
        print(e)
    finally:
        if account is not None:
            dbAPI.record_tw_unfollow(account)