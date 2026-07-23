import mysql.connector
from mysql.connector import Error
from config import * 
from logger import logger


class DatabaseManager:

    """
    Handles all database operations 
    for the RoadSense project.
    """
    def __init__(self):
        self.connection = None
        self.cursor = None
        logger.info('DatabaseManager initialized.')
    
    def create_database(self):
        """
        Create the RoadSense database if it doesn't already exist.
        """
        try:
            temp_connection = mysql.connector.connect(
                **DATABASE_CONFIG
            )

            temp_cursor = temp_connection.cursor()

            temp_cursor.execute(
                f'CREATE DATABASE IF NOT EXISTS {DB_NAME}'
            )

            temp_connection.commit()

            logger.info(f"Database '{DB_NAME}' is ready.")

            temp_cursor.close()
            temp_connection.close()

        except Error as e:
            logger.error(f'Failed to create database: {e}')


    def connect(self):
        """
        Establish a connection to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                **DATABASE_CONFIG
            )

            self.cursor = self.connection.cursor()

            logger.info('Connected to MySQL successfully.')
            return self.connection
        except Error as e:
            logger.error(f'MySQL connection failed: {e}')

            return None

    def create_tables(self):
        """
        Create all required tables for RoadSense.
        """
        
        
        try:

            sql_file = PROJECT_ROOT / 'sql' / '002_create_tables.sql'

            with open(sql_file, 'r', encoding='utf-8') as file:
                query = file.read()

            statements = query.split(';')

            for statement in statements:
                statement = statement.strip()

                if statement:
                    self.cursor.execute(statement)

            self.connection.commit()        

            logger.info("All tables created successfully.")

        except Error as e:

            logger.error(f'Failed to create tables: {e}')

    def seed_lookup_tables(self):

        """
        Insert default lookup data.
        """        
        try:

            sql_file = PROJECT_ROOT / 'sql' / '003_seed_lookup_tables.sql'

            with open(sql_file, 'r', encoding='utf-8') as file:
                query = file.read()

            for statement in query.split(';'):

                statement = statement.strip()

                if statement:

                    self.cursor.execute(statement)

            self.connection.commit()

            logger.info('Lookup tables seeded successfully.')

        except Error as e:

            logger.error(f'Failed to seed lookup tables: {e}')   

    def fetch_all(self, query):

        """
        Execute a SELECT query and return all rows.
        """

        try:
            self.cursor.execute(query)

            return self.cursor.fetchall()
        
        except Error as e:

            logger.error(f'Query failed: {e}')

            return []

    def insert_accidents(self, records):

        """
        Insert multiple accident records.
        """

        query = """

        INSERT INTO accidents (
        
        accident_date,

        hour_of_day,

        location_id,

        zone_id,

        weather_id,

        severity_id,

        road_type_id,

        latitude,

        longitude

        )

        VALUES (
        
        %s,

        %s,

        %s,

        %s,

        %s,

        %s,

        %s,

        %s,

        %s

        )

        """

        try:
            self.cursor.executemany(

            query,

            records

            )

            self.connection.commit()

            logger.info(f'{len(records)} accidents inserted.')

        except Error as e:

            self.connection.rollback()

            logger.error(f'Insertion failed: {e}')

            raise

    def disconnect(self):

        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()
        logger.info('Database connection closed.') 


if __name__ == '__main__':

    db = DatabaseManager()

    db.create_database()

    if db.connect():

        db.create_tables()

        db.seed_lookup_tables()

            

