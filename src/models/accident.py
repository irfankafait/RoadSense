from datetime import date
from pydantic import BaseModel

class Accident(BaseModel):

    """
    Represents a single accident returned by the API.
    """

    accident_id: int
    accident_date: date
    hour_of_day: int

    location: str
    zone: str
    road_type: str
    severity: str
    weather: str

    latitude: float
    longitude: float

class AccidentListResponse(BaseModel):

    """
    Response returned by GET /accidents.
    """

    success: bool
    data: list[Accident]