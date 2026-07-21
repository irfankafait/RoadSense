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
        self.zones = {}

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

        self.zones = self._load_lookup_dictionary(

            'zones',
            'zone_id',
            'zone_name'
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
    def validate_columns(self, df):

        """
        Validate that all required columns exist.

        """

        required_columns = [

            'accident_date',

            'hour_of_day',

            'location',

            'zone',

            'weather',

            'severity',

            'road_type',

            'latitude',

            'longitude'

        ]

        missing_columns = []

        for column in required_columns:

            if column not in df.columns:
                missing_columns.append(column)

        if missing_columns:

            logger.error(f'Missing required columns: {missing_columns}')

            raise ValueError(f'Missing required columns: {missing_columns}')

        logger.info('CSV validation completed successfully.')     


    def validate_row(self, row):

        """
        Validate one CSV row.
        """

        if row.location not in self.locations:
            logger.warning(f"Location '{row.location}' does not exist in the lookup table.")
            return False


        if row.zone not in self.zones:
            logger.warning(f"Zone '{row.zone}' does not exist in the lookup table.")
            return False
        

        if row.weather not in self.weather:
            logger.warning(f"Weather '{row.weather}' does not exist in the lookup table.")
            return False
        

        if row.severity not in self.severity:
            logger.warning(f"Severity '{row.severity}' does not exist in the lookup table.")
            return False
        

        if row.road_type not in self.road_types:
            logger.warning(f"Road type '{row.road_type}' does not exist in the lookup table.")
            return False
        
        if not (0<= row.hour_of_day <= 23):
            logger.warning(f"Invalid hour_of_day: {row.hour_of_day}")
            return False
        
        return True

    def transform_row(self, row):

        """
        Transform one CSV row into a database-ready tuple.
        """

        location_id = self.locations[row.location]

        weather_id = self.weather[row.weather]

        severity_id = self.severity[row.severity]

        road_type_id = self.road_types[row.road_type]

        zone_id  = self.zones[row.zone]

        return (
            row.accident_date,

            row.hour_of_day,

            location_id,

            zone_id,

            weather_id,

            severity_id,

            road_type_id,

            row.latitude,

            row.longitude

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
            
            self.validate_columns(df)

            records = []

            successful_rows = 0

            skipped_rows = 0

            # Why did we use itertuples() against interrows(), because iterrows() returns as a pandas series,
            # each row needs to converted by pandas in series object one by one. But, itertuples() returns
            # lightweight object called a named tuple. It is faster because Python does not have to perform
            # dictionary-style lookup. Switching to itertuples() is a good improvement, but the pipeline still 
            # builds a complete records list before inserting into database and it consumes a lot of memory,
            # if millions of rows there. So we need to convert it in Batch Processing. (for example, 1,000)
            # records at a time

            for index, row in enumerate(df.itertuples(index=False), start=1):

                if not self.validate_row(row):
                    logger.warning(f'Skipping row {index + 1}')

                    skipped_rows += 1

                    continue

                record = self.transform_row(row)

                records.append(record)

                successful_rows += 1

                if len(records) >= BATCH_SIZE:

                    self.load(records)

                    logger.info(f'Inserted batch of {BATCH_SIZE} records.')
                    records.clear()

            if records:
                self.load(records)

                logger.info(f'Inserted final barch of {len(records)} records.')

            logger.info(f'successfully processed: {successful_rows}')

            logger.info(f'Skipped rows: {skipped_rows}')    


        finally:
            self.db.disconnect()

            end = perf_counter()

            elapsed = end - start
            
            logger.info(f'Pipeline completed in {elapsed:.2f} seconds.')

if __name__ == '__main__':
    etl = ETLoader()
    etl.run()