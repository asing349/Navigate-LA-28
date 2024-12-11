# server/schemas/base.py

# Pydantic's base class for defining data validation and serialization schemas
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models in the application.

    This class serves as the foundation for all schemas, providing common configurations
    that ensure compatibility with SQLAlchemy ORM models.

    Attributes:
        Config (class): Inner configuration class for Pydantic schemas.
    """
    class Config:
        """
        Pydantic configuration class for schemas.

        Attributes:
            orm_mode (bool): Enables Pydantic models to work seamlessly with SQLAlchemy
                            ORM objects by treating them as dictionaries.
        """
        orm_mode = True  # Enables ORM mode to allow direct interaction with SQLAlchemy models
