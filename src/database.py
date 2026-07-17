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

if __name__ == '__main__':
    db = DatabaseManager()
            

