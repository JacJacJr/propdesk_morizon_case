import pandas as pd

from abc import ABC, abstractmethod

class PortalParser:
    def compare_columns(df, col1, col2):
        df_no_na = df.replace('NONE', pd.NA).dropna(subset=[col1, col2])
        mismatch = df_no_na[df_no_na[col1] != df_no_na[col2]]

        if mismatch.empty:
            print(f"Kolumny '{col1}' i '{col2}' są identyczne.")
        else:
            print(f"### {col1} vs {col2} ###")
            for index, row in mismatch.iterrows():
                print(f"Indeks: {index}, {col1}: {row[col1]}, {col2}: {row[col2]}")

        column_verify = df[col1] == df[col2]
        column_verify.dropna(inplace=True)
        total_count = len(column_verify)
        false_count = (~column_verify).sum()
        false_ratio = false_count / total_count if total_count != 0 else float('inf')
        print(f"Wartości boolen dla serii {col1} == {col2}: {column_verify}")
        print(f"Udział wartości False w całej kolumnie: {false_ratio}")

    def column_list(df):
        return list(df.columns)

    def complete_none(df):
        df.fillna("NONE", inplace=True)
        return df

    def delete_columns(df, columns):
        df.drop(columns, axis=1, inplace=True)
        return df


    @abstractmethod
    def parse(self, file_path):
        pass

class MorizonParser(PortalParser):
    morizon_parking_column = "parking"

    morizon_drop_columns = [
        "bath_with_wc", 
        "description", 
        "electricity", 
        "gas",
        "primery_market",
        "transaction_type",
        "water"
    ]

    column_rename_dict = {
        "prec_adress": "street",
        'platform': 'portal_name',
        'balcony': 'balcony/loggia',
        'row_price': 'price'
    }

    def parse(self, data_frame):
        df = data_frame.copy(deep=True)
        PortalParser.complete_none(df)
        
        df['parking_nan'] = df[self.morizon_parking_column ].apply(lambda x: 1 if x == 'NONE' else 0)
        df['is_parking'] = df[self.morizon_parking_column].apply(lambda x: 1 if x not in [None, 'NONE'] else 0)
        PortalParser.delete_columns(df, self.morizon_parking_column) 
        
        df.rename(columns=self.column_rename_dict, inplace=True)
        PortalParser.delete_columns(df, self.morizon_drop_columns) 

        return df

class OtodomParser(PortalParser):
    duplicated_columns = ['street.1', 'heating_type.1', 'district.1']

    otodom_parking_column = "parking_type"

    otodom_drop_columns = [
        "date_added", 
        "date_update", 
        "id_realestateagency",
        "ownership_form",
        "property_rent",
        "security",
        'windows'
    ]
    
    def parse(self, data_frame):
        df = data_frame.copy(deep=True)
        PortalParser.complete_none(df)
        PortalParser.delete_columns(df, self.duplicated_columns)
       
        df['parking_nan'] = df[self.otodom_parking_column].apply(lambda x: 1 if x in [None, 'NONE'] else 0)
        df['is_parking'] = df[self.otodom_parking_column].apply(lambda x: 1 if x not in [None, 'NONE', 0, '0'] else 0)
        
        PortalParser.delete_columns(df, self.otodom_parking_column)

        PortalParser.delete_columns(df, self.otodom_drop_columns) 

        return df

class NOParser(PortalParser):

    nn_drop_columns = [
        "date_added", 
        "date_update", 
        "electricity", 
        "gas", 
        "id_realestateagency",
        "ownership_form",
        "prec_adress",
        "property_rent",
        "saperate_wc",
        "security",
        "standard",
        'water', 
        'windows',
        'height'
    ]
    
    column_rename_dict = {
        'bulding_type': 'building_type', 
        'id_portal':'id', 
        'bulding_year': 'building_year', 
        'makret_type': 'market_type', 
        'town/city': 'city'
    }

    nn_parking_columns = [
        'no_parking_space', 
        'parking_type'
    ]

    nn_parking_not_own = [
        'brak przynależnego miejsca parkingowego',
        'parking publiczny / na ulicy',
        'możliwość wykupienia',
        'parking strzeżony w pobliżu'
    ]

    def parse(self, data_frame):
        df = data_frame.copy(deep=True)
        PortalParser.complete_none(df)

        self.process_parking_columns(df)
        df.rename(columns= self.column_rename_dict, inplace=True)
        
        PortalParser.delete_columns(df, self.nn_drop_columns) 
        PortalParser.delete_columns(df, self.nn_parking_columns) 

        return df

    def process_parking_columns(self, df):
        def determine_parking_own(parking_type):
            if parking_type == 'NONE':
                return 'NONE'
            return 0 if any(option in self.nn_parking_not_own for option in str(parking_type).split(',')) else 1

        def determine_parking_nan(parking_own):
            return 1 if parking_own == 'NONE' else 0

        def determine_is_parking(no_parking_space):
            return 1 if no_parking_space != 0 else 0

        df['parking_own'] = df['parking_type'].apply(determine_parking_own)
        df.loc[df['parking_own'] == 1, 'no_parking_space'] = 1
        df['parking_nan'] = df['parking_own'].apply(determine_parking_nan)
        df['is_parking'] = df['no_parking_space'].apply(determine_is_parking)
        df.drop(columns='parking_own', inplace = True)
