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

    def get_severe_accidents(self):

        query = """

        SELECT COUNT(*)
        FROM accidents
        WHERE severity_id =(
            SELECT severity_id
            FROM severity
            WHERE severity_name = 'Critical'
        )
        """
        
        result = self.db.fetch_all(query)

        return result[0][0]
    

    def get_peak_hour(self):

        query = """
        SELECT hour_of_day,
                COUNT(*) AS accidents
        FROM accidents
        GROUP BY hour_of_day
        ORDER BY accidents DESC
        LIMIT 1
        """

        result = self.db.fetch_all(query)

        return result[0]

    def get_top_hotspot(self):

        query = """
        SELECT
            l.location_name As location,
            COUNT(*) AS accidents
        FROM accidents a
        JOIN locations l
            ON a.location_id = l.location_id
        GROUP BY l.location_id
        ORDER BY accidents DESC
        LIMIT 1
        """

        result = self.db.fetch_all(query)

        return result[0]


    def get_dashboard_statistics(self):

        """
        Returns all dashboard statistics.
        """

        total_accidents = self.get_total_accidents()
        severe_accidents = self.get_severe_accidents()

        peak_hour = self.get_peak_hour()          # (hour, total)
        hotspot = self.get_top_hotspot()          # (location_name, total)

        return {
            "success": True,
            "data": {
                "total_accidents": total_accidents,
                "severe_accidents": severe_accidents,
                "peak_hour": {
                    "hour": peak_hour[0],
                    "accidents": peak_hour[1]
                },
                "top_hotspot": {
                    "location": hotspot[0],
                    "accidents": hotspot[1]
                }
            }
        }

    
