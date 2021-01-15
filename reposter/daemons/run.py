import os
import time
from daemons.InstaWorker import InstaWorker
from database.Database import Database
import json
from datetime import datetime
import logger

SCHEDULE_PATH = "/reposter/insta_schedule.json"
#SCHEDULE_PATH = "/home/pablo/projects/reddit_reposter/reposter/insta_schedule.json"

def run_insta_daemon():
    logger.info("Daemon context created")
    dbAPI = Database()
    children = {}
    PID = os.getppid()
    logger.info("Running insta daemon for the first time. PID:{}".format(PID))
    schedule = {}
    while True:
        try:
            if os.path.isfile(SCHEDULE_PATH):
                attemps = 0
                while not schedule:
                    try:
                        with open(SCHEDULE_PATH) as json_schedule:
                            schedule = json.load(json_schedule)
                    except Exception as e:
                        logger.error(e)
                        time.sleep(60)
                        attemps = attemps + 1
                        if attemps >= 3:
                            raise e  
                
                logger.info("Schedule file readed")
                while True:
                    if datetime.now().day != datetime.strptime(schedule["time_array"][0], '%Y-%m-%d %H:%M:%S.%f').day:
                        for worker in children.values():
                            worker.kill()
                        children = {}
                        break
                    for project in dbAPI.get_projects():
                        if not children or (not (project.project_id in children.keys())):
                            worker = InstaWorker(schedule, project, PID)
                            worker.start()
                            children[project.project_id] = worker
                    logger.info("Insta daemon:: going to sleep")
                    time.sleep(60)
                logger.info("Insta daemon:: going to sleep")
                time.sleep(60)
        except Exception as e:
            logger.error(e)
            break