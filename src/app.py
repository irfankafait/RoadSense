from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import DatabaseManager


from src.api.v1.statistics import router as statistics_router
from src.api.v1.accidents import router as accidents_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application-level resources.

    The database connection pool is created when
    FastAPI starts and closed when FastAPI shuts down.
    """
    db = DatabaseManager()
    db.connect()
    app.state.db = db
    try:
        yield
    finally:
        db.disconnect()


app = FastAPI(
    title="RoadSense API",
    version="1.0.0",
    lifespan=lifespan,
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