# reference for logging implementation
# https://realpython.com/python-logging/
# https://www.toptal.com/python/in-depth-python-logging

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from configparser import ConfigParser



parser = ConfigParser()
parser.read('configs/config.ini')
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler
def get_file_handler():
   file_handler = TimedRotatingFileHandler(parser['WEBSITE_INFO']['LOG_FILE_PATH'], when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger

