import multiprocessing
import os
import sys
import time as t
from database.Database import Database
from instagram_util.InstaUtil import InstaUtil
import logger
from datetime import datetime, timedelta

# {
#     "time_array": [
#         "2021 UMT 20:00:05", "2021 UMT 20:00:06"
#     ],
#     "actions":{
#         "2021 UMT 20:00:05": "post",
#         "2021 UMT 20:00:06": "follow"        
#     }
# }

POST_PATH_TEMPLATE = "{}{}/"

class InstaWorker(multiprocessing.Process):
    def __init__(self, schedule, project, parentPID):
        self.project = project
        self.parentPID = parentPID
        self.dbAPI = Database()
        self.schedule = schedule
        self.insta_util = InstaUtil(project.insta_config)
        self.insta_util.login(project.insta_config)
        self.project_id = project.project_id
        logger.info("Project({}):::new worker created".format(self.project_id))
        super().__init__()

    def run(self):
        while True:
            try:
                logger.info("InstaWorker:: looking for new actions to perform")
                actions = []
                if self.schedule_is_wrong():
                    logger.error("Project({}): Wrong schedule format".format(self.project_id))
                    logger.info(len(self.schedule["time_array"])
                    logger.info(len(self.schedule["actions"])
                    sys.exit()

                temp = {"time_array": [], "actions":{}}
                while not actions:
                    now = datetime.now()
                    limit = now - timedelta(minutes = 3)
                    for index, time in enumerate(self.schedule["time_array"]):
                        dt_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
                        if dt_time <= now :
                            if dt_time > limit:
                                actions.append(self.schedule["actions"][time])
                        else:
                            temp["time_array"].append(time)
                            temp["actions"][time] = self.schedule["actions"][time]
                    if not actions:
                        logger.info("InstaWorker:: going to sleep")
                        t.sleep(30)
            
                self.schedule = temp
                
                for action in actions:
                    logger.info(action)
                    #self.execute_action(action)
                
                #self.reviewExistance()
            except Exception as e:
                logger.error("Project({}):".format(self.project_id) + str(e))
    
    def schedule_is_wrong(self):
        return (not self.schedule) or (len(self.schedule["time_array"]) == 0) or (len(self.schedule["time_array"]) != len(self.schedule["actions"]))


    def execute_action(self, action):
        method = getattr(self, action, lambda: logger.error("Project({}): Invalid action".format(self.project_id)))
        return method()

    def post(self):
        
        logger.info("Project({}):Starting insta poster".format(self.project_id))
            
        try:
            post = self.dbAPI.get_next_insta_post(self.project_id)
            if post:
                path = POST_PATH_TEMPLATE.format(self.project.reddit_config["path"], post.post_id )
                self.insta_util.publish_post(path)
                self.dbAPI.record_upload_insta(post.post_id, self.project_id)
        except Exception as e:
            logger.error("Project({}):".format(self.project_id) + str(e))

        logger.info("Project({}):Insta poster finished".format(self.project_id))
    
    def discover(self):
        logger.info("Project({}):Starting insta discovering".format(self.project_id))

        if self.dbAPI.no_more_insta_accounts_to_follow(self.project_id):
            try:
                eng = self.dbAPI.get_next_insta_engagement_account(self.project_id)
                if eng:
                    followers, cursor = self.insta_util.get_followers_of(eng.username, eng.cursor)
                    eng.cursor = cursor
                    self.dbAPI.update_insta_cursor(eng)
                    self.dbAPI.add_insta_followers(followers, eng.eng_id)
            except Exception as e:
                logger.error("Project({}):".format(self.project_id) + str(e))
        
        logger.info("Project({}): Insta discovering finished".format(self.project_id))
    
    def follow(self):
        logger.info("Project({}):Starting insta following".format(self.project_id))
        try:
            account = self.dbAPI.get_next_insta_user_to_follow(self.project_id)
            if account:
                self.insta_util.follow(account.user_id)
                self.dbAPI.record_insta_follow(account)
        except Exception as e:
            logger.error("Project({}):".format(self.project_id) + str(e))
    
        logger.info("Project({}):Insta following finished".format(self.project_id))
    
    def unfollow(self):
        logger.info("Project({}):Starting insta unfollowing".format(self.project_id))
        account = None
        try:
            account = self.dbAPI.get_next_insta_user_to_unfollow(self.project_id, days = 1)
            if account:
                self.insta_util.unfollow(account.user_id)
        except Exception as e:
            logger.error(e)
        finally:
            if account is not None:
                self.dbAPI.record_insta_unfollow(account)
        logger.info("Project({}):Insta unfollowing finished".format(self.project_id))
    
    def reviewExistance(self):
        try:
            os.kill(self.parentPID, 0)
        except OSError:
            logger.info("InstaWorker::Project({}): Parent process was killed, killing myself".format(self.project_id))
            return sys.exit()