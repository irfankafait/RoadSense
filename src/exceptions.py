class DatabaseError(Exception):
    """Represents a database operation failure inside the RoadSense application."""
    def __init__(self, message="A database operation failed."):
        super().__init__(message)

        