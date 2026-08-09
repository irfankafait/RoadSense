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
        SELECT COUNT(*) AS total_accidents
        FROM accidents
        """

        result = self.db.fetch_all(query)

        return result[0]['total_accidents']

    def get_severe_accidents(self):

        """
        Return the total number of critical accidents.
        """

        query = """
        SELECT COUNT(*) AS severe_accidents
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

        return result[0]['severe_accidents']


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


    def get_accidents(
            self,
            page=1,
            page_size=20,
            severity=None,
            weather=None,
            zone=None,
            road_type=None
            ):


        """
        Return one page of accidents
        """
        conditions = []
        params = []

        if severity:
            conditions.append("s.severity_name = %s")
            params.append(severity)

        if weather:
            conditions.append("w.weather_name = %s")
            params.append(weather)

        if zone:
            conditions.append("z.zone_name = %s")
            params.append(zone)

        if road_type:
            conditions.append("rt.road_type_name = %s")
            params.append(road_type)   

        where_clause = ""

        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions) 

        offset = (page - 1) * page_size
        params.extend([page_size, offset])      

        query = f"""
        SELECT
            a.accident_id,
            a.accident_date,
            a.hour_of_day,

            l.location_name AS location,
            z.zone_name AS zone,
            rt.road_type_name AS road_type,
            s.severity_name AS severity,
            w.weather_name AS weather,

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

        {where_clause}    

        ORDER BY a.accident_date DESC

        LIMIT %s 
        OFFSET %s                 
        """

        return self.db.fetch_all(
            query, 
                tuple(params)
        )