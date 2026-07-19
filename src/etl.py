import pandas as pd
from database import DatabaseManager
from logger import logger
from config import *

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

if __name__ == '__main__':
    etl = ETLoader()
    etl.load_lookup_tables()        