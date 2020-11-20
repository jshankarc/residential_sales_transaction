import configuration as configs
import logconfig as logger

import boto3

class AWSNotificationHandler:

        def __init__(self):
            self.config = configs.Configuration()
            self.log = logger.CustomLogger(__name__).get_logger()
            self.bucket_name = self.config.getConfigValue('BUCKET_NAME')
            self.s3_extract_file_path = self.config.getConfigValue('S3_EXTRACT_FILE_PATH')

            self.s3_object = boto3.resource('s3')
            self.s3_client = boto3.client('s3')
            self.sns_object = boto3.resource('sns')
            self.sub_object = self.sns_object.Subscription('arn')

        def subscribe(self):
            self.sub_object


if __name__ == '__main__':
    anh = AWSNotificationHandler()
    anh.subscribe()