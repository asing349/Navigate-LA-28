# server/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    dob = Column(DateTime)
    country = Column(String)
