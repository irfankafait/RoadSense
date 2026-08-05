from pydantic import BaseModel

class PeakHour(BaseModel):
    hour: int
    accidents: int


class TopHotspot(BaseModel):
    location: str
    accidents: int


class StatisticsData(BaseModel):
    total_accidents: int
    severe_accidents: int
    peak_hour: PeakHour
    top_hotspot: TopHotspot


class StatisticsResponse(BaseModel):
    success: bool
    data: StatisticsData