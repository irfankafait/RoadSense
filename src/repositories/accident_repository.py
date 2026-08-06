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

    def get_severe_accidents(self):

        """
        Return the total number of critical accidents.
        """

        query = """
        SELECT COUNT(*)
        FROM accidents
        WHERE severity_id = (
            SELECT severity_id
            FROM severity
            WHERE severity_name = %s
        )
        """

        result = self.db.fetch_all(
            query,
            ('Critical',)
        )

        return result[0][0]


    def get_peak_hour(self):
        """
        Return the busiest accident hour.
        """
        query = """
        SELECT 
            hour_of_day,
            COUNT(*) AS accidents
        FROM accidents
        GROUP BY hour_of_day
        ORDER BY accidents DESC
        LIMIT 1
        """
    
        result = self.db.fetch_all(query)
    
        return result[0]
    
    def get_top_hotspot(self):

        """
        Return the location with the most accidents.
        """
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
    def get_accidents(self):

        """
        Return all accidents with desriptive names.
        """

        query = """
        SELECT
            a.accident_id,
            a.accident_date,
            a.hour_of_day,

            l.location_name,
            z.zone_name,
            rt.road_type_name,
            s.severity_name
            w.weather_name,

            a.latitude,
            a.longitude

        FROM accidents a

        INNER JOIN locations l
            ON a.location_id = l.location_id

        INNER JOIN zones z
            ON a.zone_id = z.zone_id

        INNER JOIN road_types rt
            ON a.road_type_id = rt.road_type_id

        INNER JOIN severity s
            ON a.severity_id = s.severity_id

        INNER JOIN weather w
            ON a.weather_id = w.weather_id

        ORDER BY a.accident_date DESC                  
        """

        return self.db.fetch_all(query)