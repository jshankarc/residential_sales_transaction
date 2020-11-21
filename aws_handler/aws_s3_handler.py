from configuration import Configuration
import logconfig as logger

import boto3
from botocore.exceptions import ClientError

class AWSS3Handle:
    def __init__(self):
        """Initialize Class level variables
        """
        self.config = Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.bucket_name = self.config.getConfigValue('BUCKET_NAME')
        self.s3_extract_file_path = self.config.getConfigValue('S3_EXTRACT_FILE_PATH')

        self.s3_object = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    def upload_file(self, file_path):
        """Upload File to AWS s3 bucket

        Args:
            file_path (String): Local File Path

        Returns:
            Boolean: Returns True if Upload is successful
        """
        file_name = file_path.split('/')[-1]

        try:
            self.s3_object.meta.client.upload_file(file_path, self.bucket_name, self.s3_extract_file_path + file_name)
        except ClientError as e:
            self.log.error(e, 'Failed To Upload file to s3 bucket: {}'.format(file_path))
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
            self.s3_object.meta.client.download_file(self.bucket_name, file_name, file_path)
        except ClientError as e:
            self.log.error(e.MSG_TEMPLATE, 'Failed To Download file to s3 bucket: {}'.format(file_path))
            # TODO: Trigger Notification
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
        except ClientError as e:
            self.log.error(e, 'Failed To Delete file to s3 bucket: {}'.format(file_path))
        return False
 
 
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