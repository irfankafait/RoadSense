from src.repositories.accident_repository import AccidentRepository
from src.models.statistics import(
    StatisticsResponse,
    StatisticsData,
    PeakHour,
    TopHotspot,
)

from src.models.accident import (
    Accident,
    AccidentListResponse,
)


class AccidentService:

    def __init__(self):

        self.repository = AccidentRepository()

    def get_total_accidents(self):

        """
        Return the total number of accidents.
        """

        return self.repository.get_total_accidents()
    

    def get_severe_accidents(self):

        return self.repository.get_severe_accidents()
    

    def get_peak_hour(self):

        return self.repository.get_peak_hour()

    def get_top_hotspot(self):

        return self.repository.get_top_hotspot()


    def get_dashboard_statistics(self):

        """
        Returns dashboard statistics as a Pydantic model.
        """

        total_accidents = self.get_total_accidents()
        severe_accidents = self.get_severe_accidents()
        peak_hour = self.get_peak_hour()          
        hotspot = self.get_top_hotspot()         

        return StatisticsResponse(
            success=True,
            data=StatisticsData(
                total_accidents=total_accidents,

                severe_accidents=severe_accidents,

                peak_hour=PeakHour(
                    hour=peak_hour[0],
                    accidents=peak_hour[1]
            ),

            top_hotspot=TopHotspot(
                location=hotspot[0],
                accidents=hotspot[1]
            )
        )
    )

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
        Returns a page of accidents.
        """

        rows = self.repository.get_accidents(
            page=page,
            page_size=page_size,
            severity=severity,
            weather=weather,
            zone=zone,
            road_type=road_type
        )
        accidents = []

        for row in rows:
            accidents.append(
                Accident(

                    accident_id=row[0],
                    accident_date=row[1],
                    hour_of_day=row[2],
                    location=row[3],
                    zone=row[4],
                    road_type=row[5],
                    severity=row[6],
                    weather=row[7],
                    latitude=row[8],
                    longitude=row[9]
            )
        )
                
        return AccidentListResponse(
            success=True,
            data=accidents
        )

    
