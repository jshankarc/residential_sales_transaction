# reference for logging implementation
# https://realpython.com/python-logging/
# https://www.toptal.com/python/in-depth-python-logging

import logging
import configuration as configs
import sys
from logging.handlers import TimedRotatingFileHandler

class CustomLogger:
    FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.config = configs.Configuration()

    def get_console_handler(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(CustomLogger.FORMATTER)
        return console_handler

    def get_file_handler(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        file_handler = TimedRotatingFileHandler(self.config.getConfigValue('LOG_FILE_PATH'), when='midnight')
        file_handler.setFormatter(CustomLogger.FORMATTER)
        return file_handler

    def get_logger(self):
        """[summary]

        Args:
            logger_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG) # better to have too much log than not enough
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger

