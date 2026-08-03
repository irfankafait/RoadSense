from src.database import DatabaseManager


class AccidentService:

    def __init__(self):

        self.db = DatabaseManager()

        self.db.connect()

    def get_total_accidents(self): # This function is used to get the accidents records by creating the endpoint
                                   # in app.py file.

        query = """
        SELECT COUNT(*)
        FROM accidents
        """

        result = self.db.fetch_all(query)

        return result[0][0]

    def get_severe_accident(self):

        query = """

        SELECT COUNT(*)
        FROM accidents
        WHERE severity_id =(
            SELECT severity_id
            FROM severity
            WHERE severity_name = 'Critical'
        )
        """
        print(query)
        result = self.db.fetch_all(query)

        print(result)

        return result[0][0]

    def get_peak_hour(self):

        query = """
        SELECT hour_of_day,
                COUNT(*) AS total
        FROM accidents
        GROUP BY hour_of_day
        ORDER BY total DESC
        LIMIT 1
        """

        result = self.db.fetch_all(query)

        return result[0]

    def get_top_hotspot(self):

        query = """
        SELECT
            l.location_name,
            COUNT(*) AS total
        FROM accidents a
        JOIN locations l
            ON a.location_id = l.location_id
        GROUP BY l.location_id
        ORDER BY total DESC
        LIMIT 1
        """

        result = self.db.fetch_all(query)

        return result[0]

    
