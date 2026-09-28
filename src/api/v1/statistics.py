from fastapi import APIRouter, Depends

from src.dependencies import get_accident_service
from src.services.accident_service import AccidentService
from src.models.statistics import StatisticsResponse

router = APIRouter()


@router.get(
    '/statistics',
    response_model=StatisticsResponse
)

def get_statistics(
    service: AccidentService = Depends(
        get_accident_service
        ),
):

    return service.get_dashboard_statistics()