# custom modules to handle configuration and logs
import configuration as configs
import logconfig as logger


class Transform_helper:

    @staticmethod    
    def convert_object_to_cat_type(self, df, columns):
        """
        Convert Object to Category datatype in pandas dataframe
        """
        for col in columns:
            df[col] = df[col].astype('category')

        return df            

    @staticmethod
    def convert_dtype_to_float_type(self, df, columns):
        """
        Convert object to float datatype in pandas dataframe
        """
        for col in columns:
            df[col] = df[col].astype(float)

        return df

    @staticmethod
    def convert_dtype_to_boolean_type(self, df, columns):
        """
        Convert object to boolean datatype in pandas dataframe
        """
        for col in columns:
            df[col] = df[col].astype(bool)

        return df

    @staticmethod
    def map_boolean(self, df, columns):
        """
        map yes/no to 1/0
        """
        for col in columns:
            df[col] = df[col].map({'Yes' : 1, 'No' : 0})

        return df  
        
                 
    @staticmethod
    def convert_custom_date(self, df, columns):
        """
        input -  dd/mm/yyyy
        output - dd-mm-yyyy
        since already format of the date is corrent,
        we will change '/' to '-'
        """
        for col in columns:
            df[col] = df[col].str.replace('/', '-', regex = True)

        return df
