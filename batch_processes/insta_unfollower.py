from database.Database import Database
from instagram_util.InstaUtil import InstaUtil


dbAPI = Database("db.db")

for project in dbAPI.get_projects():
    account = None
    try:
        account = dbAPI.get_next_insta_user_to_unfollow(project.project_id)
        insta_util = InstaUtil(project.insta_config)
        insta_util.unfollow(account.user_id)
    except Exception as e:
        print(e)
    finally:
        if account is not None:
            dbAPI.record_insta_unfollow(account)