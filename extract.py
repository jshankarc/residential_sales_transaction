# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger

from zipfile import ZipFile

import requests as req
import os

class Extract: 


    def __init__(self):
        """
        Initialize Configuration file 
        """
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.url = self.config.getConfigValue('URL')
        self.output_dir = self.config.getConfigValue('OUTPUT_DIR')
        self.cert = self.config.getConfigValue('CERT')


    def build_url(self):
        """
        Helper method to construct download url based on the specifications
        """
        # construct url
        url = (self.url,'/PPR-2014-04-Donegal.csv/$FILE/PPR-2014-04-Donegal.csv')

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
            output = req.get(self.donwload_url, verify=self.cert)
        except ConnectionError:
            self.log.error('{}:: Connection Error to the server: URL: {}'.format(self.__class__,self.donwload_url))


        with open(self.output_dir + self.file_name.split('/')[-1], 'wb') as f:
            f.write(output.content)
        
        self.log.info('{}:: Download Completed: URL: {}'.format(self.__class__,self.file_name))

    
    def extract(self):
        """
        Unzip if zip file downloaded
        """
        
        self.download()

        if(self.donwload_url.endswith('.zip')):
            with ZipFile(self.output_dir + self.file_name, 'r') as zip:
                zip.extractall(self.output_dir)
                self.log.info('EXTRACT:: Unzip Completed')
        
        # delete file once it is data is extracted into the directory
        if os.path.exists(self.output_dir + self.file_name):
            os.remove(self.output_dir + self.file_name)
        else:
            self.log.warning('File does exists to delete: Name: {}'.format(self.file_name))


if __name__ == '__main__':
    ext = Extract()
    ext.load_config()
    ext.extract()



