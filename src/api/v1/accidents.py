from datetime import date
from fastapi import APIRouter, HTTPException, Query
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
    location: str | None = None,
    severity: str | None = None,
    weather: str | None = None,
    zone: str | None = None,
    road_type: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    sort_by: str = Query(
        default='accident_date',
    ),
    sort_order: str = Query(
        default='desc',
    ),
):

    """
    Return a paginated list of accidents.
    """
    try:    
        return service.get_accidents(
            page=page, 
            page_size=page_size,
            location=location,
            severity=severity,
            weather=weather,
            zone=zone,
            road_type=road_type,
            start_date=start_date,
            end_date=end_date,
            sort_by=sort_by,
            sort_order=sort_order,
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
