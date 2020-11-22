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


    @staticmethod
    def add_start_month(self, df, column_name, new_column_name):
        """Add start to a new column using sales date

        Args:
            df (Dataframe): Original Dataframe
            columns (String): Column Name
            new_column_name (String): New Column Name

        Returns:
            Dataframe: Updated Dataframe
        """

        df[new_column_name] = df[column_name].apply(lambda x: '01' + x[2:10])
        
        return df

    def check_quarantine_condition(df):
        """IRISH COUNTY CHECK and NEW HOME NOT FULL MARKET VALUE

        Args:
            df (Dataframe): Original Dataframe

        Returns:
            Dataframe: Updated Dataframe
        """

        # Irish county list
        irish_counties_list = ['Galway', 'Leitrim', 'Mayo', 'Roscommon', 'Sligo', 'Carlow', 'Dublin', 'Kildare', 
        'Kilkenny', 'Laois', 'Longford', 'Louth', 'Meath', 'Offaly', 'Westmeath', 'Wexford', 
        'Wicklow', 'Clare', 'Cork', 'Kerry','Limerick', 'Tipperary', 'Waterford', 'Cavan', 'Donegal', 
        'Monaghan', 'Antrim', 'Armagh', 'Down', 'Fermanagh', 'Londonderry', 'Tyrone']

        df['quarantine_ind'] = df.county.str.lower().apply(lambda x: 0 if x in irish_counties_list else 1)
        df['quarantine_code'] = df.quarantine_ind.apply(lambda x: "NOT IRISH COUNTIES" if x == 1 else "")

        df.loc[(
                df['not_full_market_price_ind'] == 1) & 
                (df['vat_exclusion_ind'] == 1) & 
                (df['new_home_ind'] == 0), 
                ['quarantine_ind', 'quarantine_code']
            ] = [1, 'NEW HOME NOT FULL MARKET VALUE']

        return df        
