class Transform_helper:
    """This class proves a handy function to deal with type convertion or simple operations
    Note: It will be useful when dealing with large columns/features
    """

    @staticmethod    
    def convert_object_to_cat_type(self, df, columns):
        """Convert Object to Category datatype in pandas dataframe

        Args:
            df (Dataframe): Original Dataframe
            columns ([List]): List of columns

        Returns:
            Dataframe: Updated Dataframe
        """
        
        for col in columns:
            df[col] = df[col].astype('category')

        return df            

    @staticmethod
    def convert_dtype_to_float_type(self, df, columns):
        """Convert object to float datatype in pandas dataframe

        Args:
            df (Dataframe): Original Dataframe
            columns (List): List of Columns

        Returns:
            Dataframe: Updated Dataframe
        """
        
        for col in columns:
            df[col] = df[col].astype(float)

        return df

    @staticmethod
    def convert_dtype_to_boolean_type(self, df, columns):
        """Convert object to boolean datatype in pandas dataframe

        Args:
            df (Dataframe): Original Dataframe
            columns (List): List of Columns

        Returns:
            Dataframe: Updated Dataframe
        """
        
        for col in columns:
            df[col] = df[col].astype(bool)

        return df

    @staticmethod
    def map_boolean(self, df, columns):
        """map yes/no to 1/0

        Args:
            df (Dataframe): Original Dataframe
            columns (List): List of Columns

        Returns:
            Dataframe: Updated Dataframe
        """
        
        for col in columns:
            df[col] = df[col].map({'Yes' : 1, 'No' : 0})

        return df  
        
                 
    @staticmethod
    def convert_custom_date(self, df, columns):
        """Input -  dd/mm/yyyy
        Output - dd-mm-yyyy
        Since already format of the date is corrent,
        we will change '/' to '-'

        Args:
            df (Dataframe): Original Dataframe
            columns (List): List of Columns

        Returns:
            Dataframe: Updated Dataframe
        """
        
        for col in columns:
            df[col] = df[col].str.replace('/', '-', regex = True)

        return df
