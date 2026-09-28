from fastapi import Depends, Request

from src.database import DatabaseManager
from src.repositories.accident_repository import AccidentRepository
from src.services.accident_service import AccidentService


def get_database(request: Request) -> DatabaseManager:

    """
    Return the application-level DatabaseManager.

    The DatabaseManager and its connection pool are created
    when the FASTAPI application starts.
    """

    return request.app.state.db


def get_accident_repository(db: DatabaseManager = Depends(get_database),
                            ):

    """
    Create an AccidentRepository using the application's DatabaseManager.
    """

    return AccidentRepository(db=db) 

def get_accident_service(
        repository: AccidentRepository = Depends(
            get_accident_repository
        ),
):

    """
    Create an AccidentService using the accident repository.
    """

    return AccidentService(
        repository=repository
    )

