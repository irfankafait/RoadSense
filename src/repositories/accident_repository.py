from src.database import DatabaseManager

class AccidentRepository:

    """
    Handles all accident-related database queries.

    This class is responsible only for retrieving
    and storing accident data.
    """

    def __init__(self, db=None):

        """
        Initialize the repository.

        If a DatabaseManager is supplied, use it.
        Otherwise create a new one.
        """

        self.db = db or DatabaseManager()

        if db is None:
            self.db.connect()

    def get_total_accidents(self):

        """
        Return the total number of accidents.
        """

        query = """
        SELECT COUNT(*)
        FROM accidents
        """

        result = self.db.fetch_all(query)

        return result[0][0]
