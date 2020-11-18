import logconfig as log
import os
from configparser import ConfigParser

class Transform:

    def __init__(self, file_name):
        #initalize ConfigParser
        self.config_object = ConfigParser()
        self.log = log.get_logger(__name__)
        # Read Configuration file  
        try:
            with open(file_name) as file:
                self.config_object.read_file(file)
                self.config = self.config_object["WEBSITE_INFO"]
        except FileNotFoundError:
            self.log.error("Configuration File Does not exist in the root path {}".format(file_name))


    def read_files(self):
        self.log.info(self.config['OUTPUT_DIR'])
        for file in os.listdir(self.config['OUTPUT_DIR']):
            if file.endswith(".csv"):
                print(os.path.join(self.config['OUTPUT_DIR'], file))


    def transform(self):
        self

if __name__== '__main__':
    trans = Transform('configs/config.ini')
    trans.read_files()