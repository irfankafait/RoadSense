from fastapi import FastAPI

from src.api.v1.statistics import router as statistics_router

app = FastAPI(
    title="RoadSense API",
    version="1.0.0"
)

app.include_router(
    statistics_router,
    prefix="/api/v1",
    tags=["Statistics"]
)