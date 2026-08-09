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

class Pagination(BaseModel):
    """
    Contain pagination information for an API response.
    """

    page: int
    page_size: int
    total: int
    total_pages: int

class AccidentListResponse(BaseModel):

    """
    Response returned by GET /accidents.
    """

    success: bool
    data: list[Accident]
    pagination: Pagination