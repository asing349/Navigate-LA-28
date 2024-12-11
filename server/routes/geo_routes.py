# server/routes/geo_routes.py

# FastAPI modules for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession  # Asynchronous database session
from typing import List, Dict, Any  # Type hints for response models

# Import schemas for request and response validation
from schemas.review import ReviewCreate, Review, ReviewUpdate
from schemas.place import Place

# Import geospatial service functions
from services.geo_service import (
    nearest_restrooms,  # Service to find the nearest restrooms
    nearest_places,  # Service to find the nearest places
    find_direct_bus_lines,  # Service to find direct bus lines
    direct_bus_routes,  # Service to find the best direct bus route
    create_attraction_visit_plan,  # Service to create a visit plan for attractions
)

# Import database dependency for session management
from config.database import get_db

# Create an APIRouter instance for geospatial routes
router = APIRouter()


@router.get("/nearest_places/", response_model=List[Place])
async def nearest_places_route(
    lat: float,  # Latitude of the user's location
    long: float,  # Longitude of the user's location
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to retrieve the nearest places based on a user's location.

    Args:
        lat (float): Latitude of the user's location.
        long (float): Longitude of the user's location.
        db (AsyncSession): Database session for executing queries.

    Returns:
        List[Place]: A list of nearby places.

    Raises:
        HTTPException: If an unexpected error occurs (500 Internal Server Error).
    """
    try:
        return await nearest_places(db, lat, long)  # Call the service function
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/nearest_restrooms/", response_model=List[Place])
async def nearest_restrooms_route(
    lat: float,  # Latitude of the user's location
    long: float,  # Longitude of the user's location
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to retrieve the nearest restrooms based on a user's location.

    Args:
        lat (float): Latitude of the user's location.
        long (float): Longitude of the user's location.
        db (AsyncSession): Database session for executing queries.

    Returns:
        List[Place]: A list of nearby restrooms.

    Raises:
        HTTPException: If an unexpected error occurs (500 Internal Server Error).
    """
    try:
        # Call the service function
        return await nearest_restrooms(db, lat, long)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/direct_bus_routes/", response_model=Dict[str, Any])
async def direct_bus_routes_route(
    lat1: float,  # Latitude of the starting location
    long1: float,  # Longitude of the starting location
    lat2: float,  # Latitude of the destination location
    long2: float,  # Longitude of the destination location
    buffer_radius: float = 0.5,  # Radius (in miles) to search for bus stops
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to retrieve the best direct bus route between two locations.

    Args:
        lat1 (float): Latitude of the starting location.
        long1 (float): Longitude of the starting location.
        lat2 (float): Latitude of the destination location.
        long2 (float): Longitude of the destination location.
        buffer_radius (float, optional): Search radius for bus stops (default: 0.5 miles).
        db (AsyncSession): Database session for executing queries.

    Returns:
        Dict[str, Any]: Details of the optimal bus route, including lines and stops.

    Raises:
        HTTPException: If an unexpected error occurs (500 Internal Server Error).
    """
    try:
        return await direct_bus_routes(
            db=db,
            lat1=lat1,
            long1=long1,
            lat2=lat2,
            long2=long2,
            buffer_radius=buffer_radius,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/attraction_plan/", response_model=Dict[str, Any])
async def attraction_plan_route(
    lat: float,  # Latitude of the user's location
    long: float,  # Longitude of the user's location
    max_places: int = 5,  # Maximum number of attractions to include in the plan
    # Optional duration for visiting attractions
    visit_duration_hours: float | None = None,
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to generate a suggested plan for visiting nearby attractions.

    Args:
        lat (float): Latitude of the user's location.
        long (float): Longitude of the user's location.
        max_places (int, optional): Maximum number of attractions to include (default: 5).
        visit_duration_hours (float, optional): Duration (in hours) for visiting attractions.
        db (AsyncSession): Database session for executing queries.

    Returns:
        Dict[str, Any]: An itinerary with attraction details and timing.

    Raises:
        HTTPException: If an unexpected error occurs (500 Internal Server Error).
    """
    try:
        return await create_attraction_visit_plan(
            db=db,
            lat=lat,
            long=long,
            max_places=max_places,
            visit_duration_hours=visit_duration_hours,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
