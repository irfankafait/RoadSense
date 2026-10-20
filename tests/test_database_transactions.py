import mysql.connector
from mysql.connector import Error

from src.database import DatabaseManager


def test_transaction_rollback():
    """
    Verify that a failed transaction rolls back
    all changes made during that transaction.
    """

    db = DatabaseManager()

    db.connect()

    connection = None
    cursor = None

    try:

        connection = db.get_connection()

        cursor = connection.cursor()

        # --------------------------------------------------
        # Create a temporary table for this test.
        # --------------------------------------------------

        cursor.execute("""
            CREATE TEMPORARY TABLE transaction_test (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """)
        connection.commit()
        # --------------------------------------------------
        # Start the transaction.
        # --------------------------------------------------

        connection.start_transaction()

        # --------------------------------------------------
        # Step 1: Insert a valid record.
        # --------------------------------------------------

        cursor.execute("""
            INSERT INTO transaction_test (name)
            VALUES (%s)
        """, ("RoadSense Test",))

        # --------------------------------------------------
        # Step 2: Deliberately cause an error.
        #
        # name cannot be NULL.
        # --------------------------------------------------

        try:

            cursor.execute("""
                INSERT INTO transaction_test (name)
                VALUES (%s)
            """, (None,))

        except Error:

            # --------------------------------------------------
            # The second operation failed.
            # Roll back the entire transaction.
            # --------------------------------------------------

            connection.rollback()

        # --------------------------------------------------
        # Check whether the first insert was rolled back.
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM transaction_test
        """)

        result = cursor.fetchone()

        total_records = result[0]

        assert total_records == 0

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

        db.disconnect()