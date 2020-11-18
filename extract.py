from configparser import ConfigParser
import requests as req
from zipfile import ZipFile
import logging as log

class Extract: 


    def __init__(self,file_name):
        """
        Initialize Configuration file 
        """

        #initalize ConfigParser
        self.config_object = ConfigParser()

        # Read Configuration file  
        try:
            with open(file_name) as file:
                self.config_object.read_file(file)
                self.config = self.config_object["WEBSITE_INFO"]
        except FileNotFoundError:
            print("Configuration File Does not exist in the root path {}".format(file_name))

        

    def build_url(self):
        """
        Helper method to construct download url based on the specifications
        """
        # construct url
        url = (self.config['url'],'/PPR-2014-04-Donegal.csv/$FILE/PPR-2014-04-Donegal.csv')

        # url merge
        self.url_construct = ''.join(url)
        # self.url_construct = 'https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf/Downloads/PPR-ALL.zip/$FILE/PPR-ALL.zip'

        return self.url_construct
    

    def download(self):
        """
        Download files from the server
        """
        self.donwload_url = self.build_url()
        self.file_name = self.donwload_url.split('/')[-1]

        try:
            output = req.get(self.donwload_url, verify=self.config['cert'])
        except ConnectionError:
            log.error('{}:: Connection Error to the server: URL: {}'.format(self.__class__,self.donwload_url))


        with open('output/' + self.file_name.split('/')[-1], 'wb') as f:
            f.write(output.content)
        
        log.info('{}:: Download Completed: URL: {}'.format(self.__class__,self.file_name))

    
    def extract(self):
        """
        
        """
        
        self.download()

        if(self.donwload_url.endswith('.zip')):
            with ZipFile(self.file_name, 'r') as zip:
                zip.extractall()
                log.info('EXTRACT:: Unzip Completed')




if __name__ == '__main__':
    ext = Extract('config.ini')
    ext.extract()


