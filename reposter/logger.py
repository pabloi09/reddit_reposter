import logging
logging.basicConfig(filename='/reposter/batch.log',format='%(levelname)s:%(asctime)s %(message)s', level=logging.INFO)

def info(message):
    logging.info(message)

def warning(message):
    logging.warning(message)

def error(message):
    logging.error(message)
    