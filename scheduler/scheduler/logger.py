import logging
from sys import stdout

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(message)s")
    consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    return logger