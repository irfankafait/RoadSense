from fastapi import APIRouter

from src.services.accident_service import AccidentService
from src.models.statistics import StatisticsResponse

router = APIRouter()

service = AccidentService()


@router.get(
    '/statistics',
    response_model=StatisticsResponse
)

def get_statistics():

    return service.get_dashboard_statistics()