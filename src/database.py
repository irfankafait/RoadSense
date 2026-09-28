import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool

from .config import * 
from .logger import logger
from .exceptions import DatabaseError


class DatabaseManager:

    """
    Handles all database operations 
    for the RoadSense project.
    """
    def __init__(self):
        self.pool = None
        
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

            raise DatabaseError(
                "The database could not be created."
            ) from e


    def connect(self):
        """
        Create the MySQL connection pool.
        """
        try:
            self.pool = MySQLConnectionPool(
                pool_name="roadsense_pool",
                pool_size=5,
                pool_reset_session=True,
                **DATABASE_CONFIG
            )

            logger.info('MySQL connection pool created successfully.')

            return self.pool

        except Error as e:
            logger.error(f'MySQL connection pool creationfailed: {e}')

            raise DatabaseError(
                "The database connection pool could not be created."
            ) from e

    def get_connection(self):
        """
        Get a connection from the connection pool.
        """
        if self.pool is None:
            raise DatabaseError("Database connection pool is not initialized.")

        try:
            connection = self.pool.get_connection()

            logger.debug('Database connection obtained from pool.')

            return connection

        except Error as e:
            logger.error(f'Failed to get connection from pool: {e}')

            raise DatabaseError(
                "A database connection could not be obtained."
            ) from e

    def create_tables(self):
        """
        Create all required tables for RoadSense.
        """

        connection = None
        cursor = None
        
        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            sql_file = PROJECT_ROOT / 'sql' / '002_create_tables.sql'

            with open(sql_file, 'r', encoding='utf-8') as file:
                query = file.read()

            statements = query.split(';')

            for statement in statements:
                statement = statement.strip()

                if statement:
                    cursor.execute(statement)

            connection.commit()        

            logger.info("All tables created successfully.")

        except Error as e:

            logger.error(f'Failed to create tables: {e}')

            raise DatabaseError(
                "The database tables could not be created."
            ) from e

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def seed_lookup_tables(self):

        """
        Insert default lookup data.
        """  

        connection = None
        cursor = None

              
        try:

            connection = self.get_connection()
            cursor = connection.cursor()


            sql_file = PROJECT_ROOT / 'sql' / '003_seed_lookup_tables.sql'

            with open(sql_file, 'r', encoding='utf-8') as file:
                query = file.read()

            for statement in query.split(';'):

                statement = statement.strip()

                if statement:

                    cursor.execute(statement)

            connection.commit()

            logger.info('Lookup tables seeded successfully.')

        except Error as e:

            if connection:
                connection.rollback()

            logger.error(f'Failed to seed lookup tables: {e}')   

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()


    def fetch_all(self, query, params=None):

        """
        Execute a SELECT query and return all rows.
        

        Parameters
        ----------
        query : str
            SQL SELECT statement.

        params : tuple | list | None
            Optional SQL parameters used for parameterized queries.
        """

        connection = None
        cursor = None   


        try:

            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)


            if params is None:
                cursor.execute(query)

            else:
                cursor.execute(query, params)

            return cursor.fetchall()
        
        except Error as e:

            logger.error(f'Query failed: {e}')

            raise DatabaseError("The database query could not be completed.") from e

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

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

        connection = None
        cursor = None


        try:

            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.executemany(
            query,
            records

            )

            connection.commit()

            logger.info(f'{len(records)} accidents inserted.')

        except Error as e:
            if connection:
                connection.rollback()

            logger.error(f'Insertion failed: {e}')

            raise DatabaseError("The accident records could not be inserted.") from e

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def clear_accidents(self):

        """
        Remove all accident records.
        """

        connection = None
        cursor = None

        try:

            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute('TRUNCATE TABLE accidents')
            connection.commit()

            logger.info('Accidents table cleared.')
        
        except Error as e:
            if connection:
                connection.rollback()

            logger.error(f'Failed to clear accidents table: {e}')

            raise DatabaseError("The accidents table could not be cleared.") from e

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()



    def disconnect(self):

        """
        Close the connection pool.
        """

        if self.pool:

            try:

                self.pool._remove_connections()

                logger.info('Database connection pool closed.')

            except Error as e:

                logger.error(f'Failed to close database connection pool: {e}')


if __name__ == '__main__':

    db = DatabaseManager()

    db.create_database()

    if db.connect():

        db.create_tables()

        db.seed_lookup_tables()

            

