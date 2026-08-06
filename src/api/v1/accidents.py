from fastapi import APIRouter
from src.services.accident_service import AccidentService
from src.models.accident import AccidentListResponse

router = APIRouter()   # Create the Router

service = AccidentService()  # Create an instance of the AccidentService

@router.get(
    "/accidents", 
    response_model=AccidentListResponse,
)

def get_accidents(
    page: int = 1,
    page_size: int = 20,
    severity: str | None = None,
    weather: str | None = None,
    zone: str | None = None,
    road_type: str | None = None,
):

    return service.get_accidents(page=page, 
        page_size=page_size,
        severity=severity,
        weather=weather,
        zone=zone,
        road_type=road_type)