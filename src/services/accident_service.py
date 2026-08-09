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
    Pagination,
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
                    hour=peak_hour['hour_of_day'],
                    accidents=peak_hour['accidents']
            ),

            top_hotspot=TopHotspot(
                location=hotspot['location'],
                accidents=hotspot['accidents']
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
        Returns a paginated list of accidents with
        pagination metadata.
        """

        rows = self.repository.get_accidents(
            page=page,
            page_size=page_size,
            severity=severity,
            weather=weather,
            zone=zone,
            road_type=road_type,
        )

        total = self.repository.get_accidents_count(
            severity=severity,
            weather=weather,
            zone=zone,
            road_type=road_type,
        )


        accidents = [
            Accident.model_validate(row)
            for row in rows
        ]

        total_pages = (total + page_size - 1) // page_size

                
        return AccidentListResponse(
            success=True,
            data=accidents,
            pagination=Pagination(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages,
            ),
        )
    
