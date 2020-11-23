# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger

from transform.transform_helper import Transform_helper
from aws_handler import aws_s3_handler
import os
import pandas as pd
import re


class Transform:

    def __init__(self):
        """Initalize Class level variable
        """
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.output_dir = self.config.getConfigValue('OUTPUT_DIR')
        self.s3_directory = self.config.getConfigValue('S3_FILE_PATH_TRANSFORM')
        

    def download_and_delete(self, file_path_list):
        """Foward list of file paths one after the other to AWS handler 

        Args:
            file_path_list (List): List of File Locations
        """
        obj = aws_s3_handler.AWSS3Handle()
        for file_path in file_path_list:
            if obj.download_file(file_path):
                if obj.delete_file(file_path):
                    return True
                else:
                    return False
            else:
                return False

    def dataframeTypeConvertion(self, df):
        """Forwards type converstion takes to Transform Helper

        Args:
            df (Dataframe): Original Dataframe

        Returns:
            Dataframe: Updated Dataframe
        """
        # convert object to float type
        df = Transform_helper.convert_dtype_to_float_type(df, ['sales_value'])

        # convert date to mm-dd-yyyy standard
        # function help us to handle the convertion as required
        df = Transform_helper.convert_custom_date(df, ['sales_date'])

        # convert object to category type
        df = Transform_helper.convert_object_to_cat_type(df, ['county'])

        return df

    def preprocessing(self, df):
        """Data Preprocessing operation

        Args:
            df (Dataframe): Original Dataframe

        Returns:
            Dataframe: Updated Dataframe
        """
        # remove unused columns
        df.drop(['postal_code', 'property_size_desc'], axis = 1, inplace = True)

        # to lower case
        df['address'] = df['address'].str.lower()
        df['county'] = df['county'].str.lower()

        # remove starting special character and comma 
        df.sales_value = df['sales_value'].apply( lambda x: re.sub('[^\d.]', '', str(x)))

        return df

    def mapToBoolean(self, df):
        """Forwards dataframe to Map to boolean type

        Args:
            df (Dataframe): Original Datatype

        Returns:
            Dataframe: Updated Dataframe
        """
        # map YES/NO to 1/0 type
        df = Transform_helper.map_boolean(df, ['not_full_market_price_ind', 'vat_exclusion_ind'])

        # map new/second-hand properties to 1/0
        df['new_home_ind'] = df['property_desc'].apply(lambda x : 1 if x == 'New Dwelling house /Apartment' else 0)

        return df


    def transform(self, file_path_list):
        """It takes care of all the process involved to transform
        1. Invoke Download and delete files on AWS
        2. Load to Pandas Dataframe 
        3. invoke Preprocess operation
        4. Upload Processed data to S3 bucket

        Args:
            file_path_list (List): List of file paths
        """
        if self.download_and_delete(file_path_list):

            for file in file_path_list:
                # extract file name
                file_name = file.split('/')[-1]   
                # https://stackoverflow.com/a/18172249 - encoding reference
                df = pd.read_csv(self.output_dir + file_name, 
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
                                skiprows=1)

                ## preprocess dataframe
                df = self.preprocessing(df)
                self.log.info('preprocessing step completed')

                # convert datatype
                # this help in read datafame size and process it faster
                df = self.dataframeTypeConvertion(df)
                self.log.info('dataframeTypeConvertion step completed')

                # map 1/0
                df = self.mapToBoolean(df)
                self.log.info('mapToBoolean step completed')

                # add start in 'month_start' column
                df = Transform_helper.add_start_month(df, 'sales_date', 'month_start')
                self.log.info('add_start_month step completed')

                # check quarantine condition
                df = Transform_helper.check_quarantine_condition(df)
                self.log.info('check_quarantine_condition step completed')

                df.to_csv(self.output_dir + file_name, index = False)
                self.log.info('create cvs file in output directory step completed')

                obj = aws_s3_handler.AWSS3Handle()
                if obj.upload_file(self.output_dir + file_name, self.s3_directory):
                    return True
                else: 
                    return False
        else:
            return False
            
if __name__== '__main__':
    trans = Transform()
    trans.transform()