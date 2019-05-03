import logging
LOG_FORMAT= "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename='./api.log',level=logging.DEBUG,format=LOG_FORMAT,datefmt='%a, %d %b %Y %H:%M:%S')

logger=logging.getLogger()

def info(message):
    print("Info called",message)
    logger.info(str(message))