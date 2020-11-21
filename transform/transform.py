# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger

from transform.transform_helper import Transform_helper
import os
import pandas as pd


class Transform:

    def __init__(self):
        """[summary]

        Args:
            file_name ([type]): [description]
        """
        self.config = configs.Configuration()
        self.log = logger.CustomLogger(__name__).get_logger()
        self.output_dir = self.config.getConfigValue('OUTPUT_DIR')
        # Transform_helper = thelper.Transform_helper()

    def read_files(self):
        """[summary]
        """
        files_list = []
        for file in os.listdir(self.output_dir):
            if file.endswith(".csv"):
                self.log.info(os.path.join(self.output_dir, file))
                files_list.append(os.path.join(self.output_dir, file))
        
        return files_list

    def dataframeTypeConvertion(self, df):
        # convert object to float type
        df = Transform_helper.convert_dtype_to_float_type(df, ['sales_value'])

        # convert date to mm-dd-yyyy standard
        # function help us to handle the convertion as required
        df = Transform_helper.convert_custom_date(df, ['sales_date'])

        # convert object to category type
        df = Transform_helper.convert_object_to_cat_type(df, ['county'])

        return df

    def preprocessing(self, df):
        # remove unused columns
        df.drop(['address', 'postal_code', 'property_size_desc'], axis = 1, inplace = True)

        # remove starting special character and comma 
        df.sales_value = df.sales_value.str.replace('[^\d.]', '', regex = True)

        return df

    def mapToBoolean(self, df):
        # map YES/NO to 1/0 type
        df = Transform_helper.map_boolean(df, ['not_full_market_price_ind', 'vat_exclusion_ind'])

        self.log.info(df.dtypes)
        # map new/second-hand properties to 1/0
        df['new_home_ind'] = df['property_desc'].map({'New Dwelling house /Apartment' : 1, 'Second-Hand Dwelling house /Apartment' : 0})

        return df


    def transform(self):
        """[summary]

        Args:
            then ([type]): [description]
        """
        self.log.info(self.read_files())
        for file in self.read_files():
            # https://stackoverflow.com/a/18172249 - encoding reference
            df = pd.read_csv('output/PPR-ALL.csv', 
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


            ## preprocess dataframe
            df = self.preprocessing(df)

            # convert datatype
            # this help in read datafame size and process it faster
            df = self.dataframeTypeConvertion(df)

            # map 1/0
            df = self.mapToBoolean(df)


if __name__== '__main__':
    trans = Transform()
    trans.transform()