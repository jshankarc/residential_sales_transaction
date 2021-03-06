# custom modules to handle configuration and logs
from exception import InvalidRequest
import configuration as configs
import logconfig as logger

from zipfile import ZipFile

import requests as req
import shutil


from aws_handler import aws_s3_handler as ah

class Extract: 

    def __init__(self):
        """Initialize Class level objects

        Args:
            county (String): Irish County
            monthYear (String): Year and Month
        """
        
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.url = self.config.getConfigValue('URL')
        self.output_dir = self.config.getConfigValue('OUTPUT_DIR')
        self.s3_directory = self.config.getConfigValue('S3_FILE_PATH_EXTRACT')
        self.cert = self.config.getConfigValue('CERT')
        self.request_timeout = self.config.getConfigValue('REQUEST_TIMEOUT')
        self.bulkdownloadURL = self.config.getConfigValue('BULKDOWNLOAD_URL')


    def build_url(self):
        """Construct download url based on the specifications

        Returns:
            String: Download URL
        """
        # construct url
        self.file_name = 'PPR-{}-{}-{}.csv'.format(self.year, self.month, self.county)

        # url merge
        self.url_construct = '{}/{}/$FILE/{}'.format(self.url, self.file_name, self.file_name)

        # self.url_construct = ''
        self.log.info('File DOWNLOAD URL {}'.format(self.url_construct))

        return self.url_construct


    # exception handling 
    # https://stackoverflow.com/a/47007419 
    def download(self):
        """Download files from the server
        """
        #TODO: Trigger SNS Notification on failure
        #TODO: Implement Circuit Break technique
        try:
            output = req.get(self.donwload_url, verify=self.cert, stream = True, timeout= int(self.request_timeout))
            output.raise_for_status()
            if output.status_code == 200:
                with open(self.output_dir + self.file_name.split('/')[-1], 'wb') as f:
                    f.write(output.content)
        except req.exceptions.HTTPError as err:
            self.log.error('Download Failed with Http Error : {}'.format(err))
            raise InvalidRequest('This is invalid', status_code=555)
            return False
        except req.exceptions.ConnectionError as err:
            self.log.error('Download Failed with Connection Error : {}'.format(err))
            return False
        except req.exceptions.Timeout as err:
            self.log.error('Download Failed with Timeout Error: {}'.format(err))
            return False
        except req.exceptions.RequestException as err:
            self.log.error('Download Failed with OOps: Something Else: {}'.format(err))
            return False

        self.log.info('Download Completed: URL: {}'.format(self.file_name))
        return True


    def extract_workflow(self):

        if self.download():
            awsobj = ah.AWSS3Handle()

            if awsobj.upload_file(self.output_dir + self.file_name, self.s3_directory):

                if(self.donwload_url.endswith('.zip')):
                    with ZipFile(self.output_dir + self.file_name, 'r') as zip:
                        zip.extractall(self.output_dir)
                        self.log.info('EXTRACT:: Unzip Completed and deleted file')

                    # delete file once it is data is extracted into the directory
                    shutil.rmtree(self.output_dir) 
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    
    def extract(self, county, monthYear):
        """Unzip if zip file downloaded
        """
        self.year = monthYear.split('-')[0]
        self.month = monthYear.split('-')[1]
        self.county = county

        self.donwload_url = self.build_url()

        return self.extract_workflow()

    def extract_zip(self):
        self.donwload_url = self.bulkdownloadURL

        self.file_name = self.bulkdownloadURL.split('/')[-1]

        return self.extract_workflow()


if __name__ == '__main__':
    ext = Extract()
    ext.extract()



