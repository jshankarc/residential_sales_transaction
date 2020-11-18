from zipfile import ZipFile
from configparser import ConfigParser

import requests as req
# import logging as log
import os
import logconfig as log

class Extract: 


    def __init__(self,file_name):
        """
        Initialize Configuration file 
        """
        self.file_name = file_name
        self.log = log.get_logger(__name__)

    def load_config(self):
        """

        """
        
        #initalize ConfigParser
        self.config_object = ConfigParser()

        # Read Configuration file  
        try:
            with open(self.file_name) as file:
                self.config_object.read_file(file)
                self.config = self.config_object["WEBSITE_INFO"]
                self.log.info(self.config['URL'])
        except FileNotFoundError:
            self.log.error("Configuration File Does not exist in the root path {}".format(self.file_name))

        

    def build_url(self):
        """
        Helper method to construct download url based on the specifications
        """
        # construct url
        url = (self.config['URL'],'/PPR-2014-04-Donegal.csv/$FILE/PPR-2014-04-Donegal.csv')

        # url merge
        self.url_construct = ''.join(url)
        self.url_construct = 'https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf/Downloads/PPR-ALL.zip/$FILE/PPR-ALL.zip'

        return self.url_construct
    

    def download(self):
        """
        Download files from the server
        """
        self.donwload_url = self.build_url()
        self.file_name = self.donwload_url.split('/')[-1]

        try:
            output = req.get(self.donwload_url, verify=self.config['CERT'])
        except ConnectionError:
            self.log.error('{}:: Connection Error to the server: URL: {}'.format(self.__class__,self.donwload_url))


        with open(self.config['OUTPUT_DIR'] + self.file_name.split('/')[-1], 'wb') as f:
            f.write(output.content)
        
        self.log.info('{}:: Download Completed: URL: {}'.format(self.__class__,self.file_name))

    
    def extract(self):
        """
        Unzip if zip file downloaded
        """
        
        self.download()

        if(self.donwload_url.endswith('.zip')):
            with ZipFile(self.config['OUTPUT_DIR'] + self.file_name, 'r') as zip:
                zip.extractall(self.config['OUTPUT_DIR'])
                self.log.info('EXTRACT:: Unzip Completed')
        
        # delete file once it is data is extracted into the directory
        if os.path.exists(self.config['OUTPUT_DIR'] + self.file_name):
            os.remove(self.config['OUTPUT_DIR'] + self.file_name)
        else:
            self.log.warning('File does exists to delete: Name: {}'.format(self.file_name))


if __name__ == '__main__':
    ext = Extract('configs/config.ini')
    ext.load_config()
    ext.extract()


