from fastapi import APIRouter, Query
from src.services.accident_service import AccidentService
from src.models.accident import AccidentListResponse

router = APIRouter()   # Create the Router

service = AccidentService()  # Create an instance of the AccidentService

@router.get(
    "/accidents", 
    response_model=AccidentListResponse,
)

def get_accidents(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    severity: str | None = None,
    weather: str | None = None,
    zone: str | None = None,
    road_type: str | None = None,
):

    """
    Return a paginated list of accidents.
    """

    return service.get_accidents(
        page=page, 
        page_size=page_size,
        severity=severity,
        weather=weather,
        zone=zone,
        road_type=road_type,
        )