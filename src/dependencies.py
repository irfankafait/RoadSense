from src.database import DatabaseManager
from src.repositories.accident_repository import AccidentRepository
from src.services.accident_service import AccidentService


def get_database():

    """
    Create a database manager for the current request.
    """

    db = DatabaseManager()

    connection = db.connect()

    if connection is None:
        raise RuntimeError(
            "Database connection could not be established.")

    try:
        yield db

    finally:

        db.disconnect()

def get_accident_repository(db: DatabaseManager):

    """
    Create an AccidentRepository using the request's database manager.
    """

    return AccidentRepository(db=db) 

def get_accident_service(
        repository: AccidentRepository
):

    """
    Create an AccidentService using the request's accident repository.
    """

    return AccidentService(
        repository=repository
    )

    