import pandas as pd
from database import DatabaseManager
from logger import logger
from config import *
from time import perf_counter

class ETLoader:
    
    """
    Handles the Extract,
    Transform,
    and Load process.
    """

    def __init__(self):
        
        self.db = DatabaseManager()

        self.db.connect()

        self.locations = {}
        self.weather = {}
        self.severity = {}
        self.road_types = {}

        logger.info('ETL Loader initialized.')

    def load_lookup_tables(self):
        
        """
        Load lookup tables into dictionaries.
        """    
        self.locations = self._load_lookup_dictionary(

            'locations',
            'location_id',
            'location_name'
        )

        self.weather = self._load_lookup_dictionary(

            'weather',
            'weather_id',
            'weather_name'
        )

        self.severity = self._load_lookup_dictionary(

            'severity',
            'severity_id',
            'severity_name'
        )

        self.road_types = self._load_lookup_dictionary(

            'road_types',
            'road_type_id',
            'road_type_name'
        )

        logger.info('Lookup dictionaries loaded successfully.')

    def _load_lookup_dictionary(   
        self,
        table_name,
        id_column,
        name_column
    ):
        
        """
        Load any lookup table into a dictionary.
        """
        query = f"""
            SELECT {id_column},
                   {name_column}
            FROM
                    {table_name}
        """ 

        rows = self.db.fetch_all(query)

        return {

            name: record_id

            for record_id, name in rows
        }

    def transform_row(self, row):

        """
        Transform one CSV row into a database-ready tuple.
        """

        location_id = self.locations[row['location']]

        weather_id = self.weather[row['weather']]

        severity_id = self.severity[row['severity']]

        road_type_id = self.road_types[row['road_type']]

        return (
            row['accident_date'],

            location_id,

            weather_id,

            severity_id,

            road_type_id
        )
    

    def load(self, records):

        """
        Load transformed records into the database.
        """
        self.db.insert_accidents(records)


    def run(self):

        """
        Execute the complete ETL pipeline.
        """ 

        if not self.db.connect():

            logger.error('Database connection failed.')

            return
        start = perf_counter()

        try:
            self.load_lookup_tables()

            df = pd.read_csv(PROCESSED_DATA_DIR / 'cleaned_accidents.csv')
            
            records = []

            for _, row in df.iterrows():
                record = self.transform_row(row)
                records.append(record)

            print(records[:10])
            self.load(records)

        finally:
            self.db.disconnect()

            end = perf_counter()

            elapsed = end - start
            
            logger.info(f'Pipeline completed in {elapsed:.2f} seconds.')

if __name__ == '__main__':
    etl = ETLoader()
    etl.run()