from fastapi import Depends, Request

from src.database import DatabaseManager
from src.repositories.accident_repository import AccidentRepository
from src.services.accident_service import AccidentService


def get_database(request: Request) -> DatabaseManager:
    """
    Return the application-level DatabaseManager.
    """
    return request.app.state.db


def get_accident_repository(
    db: DatabaseManager = Depends(get_database),
):
    """
    Create a repository using the application database manager.
    """
    return AccidentRepository(db=db)


def get_accident_service(
    db: DatabaseManager = Depends(get_database),
    repository: AccidentRepository = Depends(
        get_accident_repository
    ),
):
    """
    Create a service using the repository and database manager.
    """
    return AccidentService(
        repository=repository,
        db=db,
    )