# reference for logging implementation
# https://realpython.com/python-logging/
# https://www.toptal.com/python/in-depth-python-logging

import logging
import configuration as configs
import sys
from logging.handlers import TimedRotatingFileHandler

class CustomLogger:

    def __init__(self, logger_name):
        """Load configuration upon object creating

        Args:
            logger_name (String): Class Name to print in log file
        """
        self.logger_name = logger_name
        self.config = configs.Configuration()
        self.format = configs.getConfigValue('LOG_FORMAT')

    def get_console_handler(self):
        """This helps print message on console 

        Returns:
            Object: Console handler object
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.format)
        return console_handler

    def get_file_handler(self):
        """load logs messages to a file

        Returns:
            Object: File handler object
        """
        file_handler = TimedRotatingFileHandler(self.config.getConfigValue('LOG_FILE_PATH'), when='midnight')
        file_handler.setFormatter(self.format)
        return file_handler

    def get_logger(self):
        """Logger object handler

        Returns:
            Object: Logger object
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG) # better to have too much log than not enough
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger

