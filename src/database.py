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
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD
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
                host = DB_HOST,
                port = DB_PORT,
                database = DB_NAME,
                user = DB_USER,
                password = DB_PASSWORD
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
        sql_file = PROJECT_ROOT / 'sql' / '002_create_tables.sql'
        
        with open(sql_file, 'r', encoding='utf-8') as file:
            query = file.read()
        
        
        try:

            self.cursor.execute(query)

            self.connection.commit()

            logger.info("Table 'accidents' created successfully.")

        except Error as e:

            logger.error(f'Failed to create table: {e}')


if __name__ == '__main__':
    db = DatabaseManager()

    db.create_database()

    if db.connect():
        db.create_tables()
            

