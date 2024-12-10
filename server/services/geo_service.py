# server/services/review_service.py
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func

from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, ReviewUpdate
from services.nearest_places import find_nearest_places
from services.nearest_restrooms import find_nearest_restrooms
from schemas.place import Place
from models.place import Place as PlaceModel


async def nearest_places(db: AsyncSession, lat: float, long: float) -> List[Place]:
    # Get nearest places from Spark
    spark_places = find_nearest_places(lat, long, 10)

    places = []
    for row in spark_places:
        # Query database to find matching place using name and coordinates
        query = select(PlaceModel).where(
            and_(
                PlaceModel.name == row.name,
                func.abs(PlaceModel.latitude - float(row.latitude))
                < 0.0001,  # Small threshold for float comparison
                func.abs(PlaceModel.longitude - float(row.longitude)) < 0.0001,
                PlaceModel.types == "tourist attraction",
            )
        )
        result = await db.execute(query)
        db_place = result.scalar_one_or_none()
        if db_place:
            place_dict = {
                "id": db_place.id,
                "name": db_place.name,
                "description": db_place.description,
                "latitude": db_place.latitude,
                "longitude": db_place.longitude,
                "address": db_place.address,
                "types": db_place.types,
            }
            places.append(Place(**place_dict))

    return places


async def nearest_restrooms(db: AsyncSession, lat: float, long: float) -> List[Place]:
    # Get nearest restrooms from Spark
    spark_restrooms = find_nearest_restrooms(lat, long, 10)

    restrooms = []
    for row in spark_restrooms:
        # Query database to find matching restroom using coordinates
        query = select(PlaceModel).where(
            and_(
                PlaceModel.name == row.name,
                func.abs(PlaceModel.latitude - float(row.latitude))
                < 0.0001,  # Small threshold for float comparison
                func.abs(PlaceModel.longitude - float(row.longitude)) < 0.0001,
                PlaceModel.types == "restroom",
            )
        )
        result = await db.execute(query)
        db_restroom = result.scalar_one_or_none()
        if db_restroom:
            restroom_dict = {
                "id": db_restroom.id,
                "name": db_restroom.name,
                "description": db_restroom.description,
                "latitude": db_restroom.latitude,
                "longitude": db_restroom.longitude,
                "address": db_restroom.address,
                "types": db_restroom.types,
            }
            restrooms.append(Place(**restroom_dict))

    return restrooms
