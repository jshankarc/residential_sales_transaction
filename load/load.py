# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger

from transform.transform_helper import Transform_helper
from aws_handler import aws_s3_handler
import os
import pandas as pd

class Load:
    def __init__(self, file_path):
        """Initalize Class level variable
        """
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.output_dir = self.config.getConfigValue('OUTPUT_DIR')
        self.s3_loadpath = self.config.getConfigValue('S3_FILE_PATH_LOAD')
        self.s3_processed_file = self.config.getConfigValue('FINAL_ETL_PROCCESSED_FILE')
        self.file_path = file_path

    def load(self):
        """Loads data to s3 after amending changes

        Returns:
            Boolean: Success or failure
        """
        awsObj = aws_s3_handler.AWSS3Handle()
        if awsObj.download_file(self.s3_loadpath + self.s3_processed_file):

            if awsObj.download_file(self.file_path):
                for file in self.file_path:
                    # extract file name
                    file_name = self.file_path.split('/')[-1]   
                    # https://stackoverflow.com/a/18172249 - encoding reference
                    df_new = pd.read_csv(self.output_dir + file_name, 
                                    encoding = "ISO-8859-1", 
                                    names=[
                                        'sales_date', 
                                        'address', 
                                        'postal_code', 
                                        'county', 
                                        'sales_value', 
                                        'not_full_market_price_ind', 
                                        'vat_exclusion_ind', 
                                        'property_desc', 
                                        'property_size_desc' ], 
                                    nrows=20, 
                                    skiprows=1)

                    df_old = pd.read_csv(self.s3_loadpath + self.s3_processed_file, 
                                    encoding = "ISO-8859-1", 
                                    names=[
                                        'sales_date', 
                                        'address', 
                                        'postal_code', 
                                        'county', 
                                        'sales_value', 
                                        'not_full_market_price_ind', 
                                        'vat_exclusion_ind', 
                                        'property_desc', 
                                        'property_size_desc' ], 
                                    nrows=20, 
                                    skiprows=1)

                    pd.concat([df_new, df_old]).drop_duplicates().reset_index(drop=True)

                    if awsObj.upload_file(self.s3_loadpath + self.s3_processed_file, self.s3_processed_file):
                        return True
                    else: 
                        return False

                return True
            else:
                return False
        else:
            return False


if __name__== '__main__':
    trans = Load()
    trans.load()