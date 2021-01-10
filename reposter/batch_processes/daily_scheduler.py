from crontab import CronTab
import os
import random

COMMAND_TEMPLATE = "python /reposter/batch_processes/{} >> /reposter/batch.log 2>&1" 

class Scheduler:

    def __init__(self, user):
        os.system("crontab -r -u {}".format(user))
        self.cron = CronTab(user=user)
        self.schedule_job_on(command=COMMAND_TEMPLATE.format("daily_scheduler.py"), hours = 0, minutes = 0)
        self.follow_dist = self.get_follow_distribution()
        self.repost_dist = self.get_repost_distribution()
    
    def make_daily_schedule(self):
        self.make_core_schedule()
        self.make_insta_engagement_schedule()
        self.make_tw_engagement_schedule()
        self.make_repost_schedule()

    def make_core_schedule(self):
        self.schedule_job_on(command=COMMAND_TEMPLATE.format("downloader.py"), hours = 0, minutes = 5)
        self.schedule_job_on(command=COMMAND_TEMPLATE.format("downloader.py"), hours = 12, minutes = 5)
        self.schedule_job_every(command=COMMAND_TEMPLATE.format("file_cleaner.py"), hours = 1, minutes = 30)
        self.schedule_job_every(command=COMMAND_TEMPLATE.format("tw_discoverer.py"), hours = 1, minutes = 5)
        self.schedule_job_every(command=COMMAND_TEMPLATE.format("insta_discoverer.py"), hours = 1, minutes = 5)
    
    def make_insta_engagement_schedule(self):
        number_of_follows = random.randint(160,190)
        times = random.sample(self.follow_dist, number_of_follows)
        for (hours, minutes) in times:
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("insta_follower.py"), hours = hours, minutes = minutes)

        times = random.sample(self.follow_dist, number_of_follows)
        for (hours, minutes) in times:
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("insta_unfollower.py"), hours = hours, minutes = minutes)

        
    def make_tw_engagement_schedule(self):
        number_of_follows = random.randint(380,400)
        times = random.sample(self.follow_dist, number_of_follows)
        for (hours, minutes) in times:
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("tw_follower.py"), hours = hours, minutes = minutes)

        times = random.sample(self.follow_dist, number_of_follows)
        for (hours, minutes) in times:
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("tw_unfollower.py"), hours = hours, minutes = minutes)

    def make_repost_schedule(self):
        number_of_posts = 10
        times = random.sample(self.repost_dist[0], number_of_posts)
        for (hours, minutes) in times:
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("twitter_poster.py"), hours = hours, minutes = minutes)
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("insta_poster.py"), hours = hours, minutes = minutes + 10)

        times = random.sample(self.repost_dist[1], number_of_posts)
        for (hours, minutes) in times:
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("twitter_poster.py"), hours = hours, minutes = minutes)
            self.schedule_job_on(command=COMMAND_TEMPLATE.format("insta_poster.py"), hours = hours, minutes = minutes + 10)

    def schedule_job_on(self, command, hours, minutes):
        job = self.cron.new(command=command)
        job.hour.on(hours)
        job.minute.on(minutes)
        self.cron.write()
    
    def schedule_job_every(self, command, hours, minutes):
        job = self.cron.new(command=command)
        job.hour.every(hours)
        job.minute.on(minutes)
        self.cron.write()
    
    def get_follow_distribution(self):
        values = []
        for hours in range(0,24):
            if hours != 0:
                for minutes in range(0,60):
                    values.append((hours,minutes))
            else:
                for minutes in range(10,60):
                    values.append((hours,minutes))
        return values
    
    def get_repost_distribution(self):
        first_shift = []
        second_shift = []
        for hours in range(0,24):
            if hours != 0 and hours != 12:
                for minutes in range(0,50):
                    if hours < 12:
                        first_shift.append((hours,minutes))
                    else:
                        second_shift.append((hours,minutes))
            else:
                for minutes in range(10,50):
                    if hours < 12:
                        first_shift.append((hours,minutes))
                    else:
                        second_shift.append((hours,minutes))
        return [first_shift, second_shift]

scheduler = Scheduler("root")
scheduler.make_daily_schedule()








