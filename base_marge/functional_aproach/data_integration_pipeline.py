#1. load dirty data
#2. save data backups
import pandas as pd
from propdesk.base_marge.functional_aproach.parsers import MorizonParser, OtodomParser, NOParser

class DataIntegrationPipeline:
    def process_data():

        morizon_csv_path = "data/morizon/morizon.csv"
        morizon_raw = pd.read_csv(morizon_csv_path)
        morizon_parser = MorizonParser()
        morizon_data = morizon_parser.parse(morizon_raw)
        morizon_data.head(10)

        otodom_csv_path = "data/otodom/otodom.csv"
        otodom_raw = pd.read_csv(otodom_csv_path)
        otodom_parser = OtodomParser()
        otodom_data = otodom_parser.parse(otodom_raw)
        otodom_data.head(10)

        no_csv_path = "data/no/no.csv"
        no_raw = pd.read_csv(no_csv_path)
        no_parser = NOParser()
        no_data = no_parser.parse(no_raw)
        no_data.head(10)
        
        all_platforms = pd.DataFrame()
        all_platforms = pd.concat([morizon_data, otodom_data, no_data], ignore_index=True)
        all_platforms.to_csv("data/archive/all_platforms.csv", index=False)
        all_platforms.info()

DataIntegrationPipeline.process_data()
