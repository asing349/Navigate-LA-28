# server/schemas/base.py
from pydantic import BaseModel
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True