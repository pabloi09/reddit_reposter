import daemon
import lockfile

SCHEDULE_PATH = "/reposter/insta_schedule.json"
#SCHEDULE_PATH = "/home/pablo/projects/reddit_reposter/reposter/insta_schedule.json"
WORKING_DIRECTORY = "/reposter/"
#WORKING_DIRECTORY = "/home/pablo/projects/reddit_reposter/reposter/"
PID_FILE = WORKING_DIRECTORY + "insta_daemon.pid"


with daemon.DaemonContext(working_directory = WORKING_DIRECTORY, 
                          umask = 0o002, 
                          pidfile = lockfile.FileLock(PID_FILE)) as context:
    from daemons.run import run_insta_daemon
    run_insta_daemon()
    
        

        


