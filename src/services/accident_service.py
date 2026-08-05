from src.repositories.accident_repository import AccidentRepository
from src.models.statistics import(
    StatisticsResponse,
    StatisticsData,
    PeakHour,
    TopHotspot,
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

    
