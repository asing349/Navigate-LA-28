# server/services/review_service.py
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
import random

from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, ReviewUpdate
from services.nearest_places import find_nearest_places
from services.nearest_restrooms import find_nearest_restrooms
from schemas.place import Place
from models.place import Place as PlaceModel
from services.nearest_bustops import find_direct_bus_lines


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in miles.
    """
    R = 3959  # Earth's radius in miles

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance, 2)  # Round to 2 decimal places


async def nearest_places(db: AsyncSession, lat: float, long: float) -> List[Place]:
    # Get nearest places from Spark
    spark_places = find_nearest_places(lat, long, 10)

    places = []
    for row in spark_places:
        # Query database to find matching place using name and coordinates
        query = select(PlaceModel).where(
            and_(
                PlaceModel.name == row.name,
                func.abs(PlaceModel.latitude - float(row.latitude)) < 0.0001,
                func.abs(PlaceModel.longitude - float(row.longitude)) < 0.0001,
                PlaceModel.types == "tourist attraction",
            )
        )
        result = await db.execute(query)
        db_place = result.scalar_one_or_none()
        if db_place:
            # Calculate distance
            distance = calculate_distance(
                lat, long, db_place.latitude, db_place.longitude
            )

            place_dict = {
                "id": db_place.id,
                "name": db_place.name,
                "description": db_place.description,
                "latitude": db_place.latitude,
                "longitude": db_place.longitude,
                "address": db_place.address,
                "types": db_place.types,
                "distance": distance,  # Add distance to the dictionary
            }
            places.append(Place(**place_dict))

    # Sort places by distance
    places.sort(key=lambda x: x.distance)
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
                func.abs(PlaceModel.latitude - float(row.latitude)) < 0.0001,
                func.abs(PlaceModel.longitude - float(row.longitude)) < 0.0001,
                PlaceModel.types == "restroom",
            )
        )
        result = await db.execute(query)
        db_restroom = result.scalar_one_or_none()
        if db_restroom:
            # Calculate distance
            distance = calculate_distance(
                lat, long, db_restroom.latitude, db_restroom.longitude
            )

            restroom_dict = {
                "id": db_restroom.id,
                "name": db_restroom.name,
                "description": db_restroom.description,
                "latitude": db_restroom.latitude,
                "longitude": db_restroom.longitude,
                "address": db_restroom.address,
                "types": db_restroom.types,
                "distance": distance,  # Add distance to the dictionary
            }
            restrooms.append(Place(**restroom_dict))

    # Sort restrooms by distance
    restrooms.sort(key=lambda x: x.distance)
    return restrooms


async def direct_bus_routes(
    db: AsyncSession,
    lat1: float,
    long1: float,
    lat2: float,
    long2: float,
    buffer_radius: float = 0.5,
) -> Dict[str, Any]:
    try:
        # Get best bus route from Spark
        route_data = await find_direct_bus_lines(
            user_lat=lat1,
            user_lon=long1,
            target_lat=lat2,
            target_lon=long2,
            buffer_radius_miles=buffer_radius,
        )

        # Check if a route was found
        if "message" in route_data:
            return {"message": "No direct bus routes found"}

        return route_data

    except Exception as e:
        print(str(e))
        raise


async def create_attraction_visit_plan(
    db: AsyncSession,
    lat: float,
    long: float,
    max_places: int = 5,
    visit_duration_hours: float | None = None,
) -> Dict[str, Any]:
    """
    Creates a plan to visit nearby attractions.

    Args:
        db: Database session
        lat: Starting latitude
        long: Starting longitude
        max_places: Maximum number of places to include in plan
        visit_duration_hours: Optional total duration of the visit in hours.
                            If None, duration will be calculated based on number of places.

    Returns:
        Dictionary containing the visit plan with suggested order and timing
    """
    # Get nearby places
    places = await nearest_places(db, lat, long)

    if not places:
        return {"message": "No attractions found nearby"}

    # Limit number of places
    places = places[:max_places]

    # If no duration specified, calculate based on number of places
    # Assuming average 1-2 hours per attraction
    if visit_duration_hours is None:
        visit_duration_hours = len(places) * random.uniform(1.0, 2.0)

    # Generate random weights for each place
    weights = [random.uniform(0.5, 1.5) for _ in places]
    total_weights = sum(weights)

    # Normalize weights to match total duration
    visit_times = [w * visit_duration_hours / total_weights for w in weights]

    # Create itinerary
    current_time = datetime.now().replace(hour=9, minute=0)  # Start at 9 AM
    itinerary = []

    for place, duration in zip(places, visit_times):
        visit = {
            "place": {
                "name": place.name,
                "address": place.address,
                "description": place.description,
                "distance_from_start": place.distance,
                "latitude": place.latitude,
                "longitude": place.longitude,
            },
            "start_time": current_time.strftime("%I:%M %p"),
            "end_time": (current_time + timedelta(hours=duration)).strftime("%I:%M %p"),
            "suggested_duration": f"{duration:.1f} hours",
        }

        itinerary.append(visit)
        current_time += timedelta(hours=duration)

    return {
        "total_attractions": len(places),
        "total_duration": f"{visit_duration_hours} hours",
        "start_location": {"latitude": lat, "longitude": long},
        "itinerary": itinerary,
    }
