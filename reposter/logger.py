import logging

LOGGER_PATH = '/reposter/batch.log'
#LOGGER_PATH = '/home/pablo/projects/reddit_reposter/reposter/batch.log'
logging.basicConfig(filename=LOGGER_PATH,format='%(levelname)s:%(asctime)s %(message)s', level=logging.INFO)

def info(message):
    logging.info(message)

def warning(message):
    logging.warning(message)

def error(message):
    logging.error(message)
    