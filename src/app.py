from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from src.api.v1.statistics import router as statistics_router
from src.api.v1.accidents import router as accidents_router
from src.exceptions import DatabaseError


app = FastAPI(
    title="RoadSense API",
    version="1.0.0"
)

@app.exception_handler(DatabaseError)
async def database_error_handler(
    request: Request, exc: DatabaseError
):
    """
    Convert RoadSense database error into
    a safe HTTP response.
    """
    return JSONResponse(
        status_code=503,
        content={
            'success': False,
            'error': {
                'code': 'DATABASE_UNAVAILABLE',
                'message': str(exc),
            }
        }
         
    )

app.include_router(
    statistics_router,
    prefix="/api/v1",
    tags=["Statistics"]
)

app.include_router(
    accidents_router,
    prefix="/api/v1",
    tags=["Accidents"]
)