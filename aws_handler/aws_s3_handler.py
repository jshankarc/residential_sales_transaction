from exception import InvalidRequest
from configuration import Configuration
import logconfig as logger

import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import S3TransferFailedError, S3UploadFailedError, Boto3Error

class AWSS3Handle:
    def __init__(self):
        """Initialize Class level variables
        """
        self.config = Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.bucket_name = self.config.getConfigValue('BUCKET_NAME')
        
        self.output_dir = self.config.getConfigValue('OUTPUT_DIR')

        self.s3_object = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    def upload_file(self, file_path, s3_directory):
        """Upload File to AWS s3 bucket

        Args:
            file_path (String): Local File Path

        Returns:
            Boolean: Returns True if Upload is successful
        """
        file_name = file_path.split('/')[-1]

        try:
            self.s3_object.meta.client.upload_file(file_path, self.bucket_name, s3_directory + file_name)
        except S3UploadFailedError as e:
            self.log.error('Failed To Upload file to s3 bucket: {}'.format(str(e)))
            return False
        except Boto3Error as e:
            self.log.error('OOps, Something else in s3 bucket: {}'.format(str(e)))
            return False
        return True
 

    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    def download_file(self, file_path):
        """Download File from AWS S3 Bucket

        Args:
            file_path (String): S3 Bucket File Location

        Returns:
            Boolean: Returns True if Download successful
        """
        # extract file name
        file_name = file_path.split('/')[-1]

        try:
            self.s3_client.download_file(self.bucket_name, file_path, self.output_dir + file_name)
        except S3TransferFailedError as e:
            self.log.error('Failed To Download file to s3 bucket: {}'.format(str(e)))
            # TODO: Trigger Notification
            return False
        except Boto3Error as e:
            self.log.error('OOps somethings else, s3 bucket: {}'.format(str(e)))
            # TODO: Trigger Notification
            return False
        except ClientError as e:
            self.log.error('OOps somethings else, s3 bucket: {}'.format(str(e)))
            return False
        return True        

    def delete_file(self, file_path):
        """Delete File in AWS S3 Bucket

        Args:
            file_path (String): S3 Bucket Location

        Returns:
            Boolean: Return True if Donwload successful
        """
        try:
            response = self.s3_client.delete_object(
            Bucket = self.bucket_name,
                Key = file_path
            )
        except S3TransferFailedError as e:
            self.log.error('Failed To Delete file to s3 bucket: {}'.format(str(e)))
            # TODO: Trigger Notification
            return False
        except Boto3Error as e:
            self.log.error('OOps somethings else, s3 bucket: {}'.format(str(e)))
            # TODO: Trigger Notification
            return False
        return True


 
if __name__== '__main__':
    s3 = boto3.client('s3')

    obj = AWSS3Handle()
    # download file from s3 bucket
    obj.download_file('extract/PPR-2014-04-Donegal.csv')

    # update file to s3 bucket
    # obj.upload_file('output/PPR-2014-04-Donegal1.csv')
    # obj.upload_file('temp.py', 'temp.py')

    # delete file form s3 bucket
    # print(obj.delete_file('temp.txt'))