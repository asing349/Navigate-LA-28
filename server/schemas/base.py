# server/schemas/base.py
from pydantic import BaseModel

class BaseSchema(BaseModel):
    """
    Base schema to be inherited by all other Pydantic schemas.
    Configures `orm_mode` for compatibility with SQLAlchemy models.
    """
    class Config:
        orm_mode = True  # Enable ORM mode to work seamlessly with SQLAlchemy models
