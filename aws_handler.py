import configuration as configs
import logconfig as logger

import boto3
from botocore.exceptions import ClientError
from moto import mock_cloudwatch

class AWSHandle:
    def __init__(self):
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()


    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    def upload_file(self,file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            self.log.error(e)
            return False
        return True    

 
if __name__== '__main__':
    s3 = boto3.client('s3')
    with open('output/temp.txt', "rb") as f:
        s3.upload_fileobj(f, 'residential-sales-transaction','temp.txt')