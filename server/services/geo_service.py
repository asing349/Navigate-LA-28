# server/services/review_service.py
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, ReviewUpdate
from services.nearest_places import find_nearest_places
from services.nearest_restrooms import find_nearest_restrooms


async def nearest_places(db: AsyncSession, lat: float, long: float) -> Dict[str, Any]:
    places = find_nearest_places(lat, long, 10)
    print(places)
    return places


async def nearest_restrooms(
    db: AsyncSession, lat: float, long: float
) -> Dict[str, Any]:
    restrooms = find_nearest_restrooms(lat, long, 10)
    return restrooms
