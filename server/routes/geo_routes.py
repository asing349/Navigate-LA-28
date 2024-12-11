from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from schemas.review import ReviewCreate, Review, ReviewUpdate
from schemas.place import Place
from services.geo_service import (
    nearest_restrooms,
    nearest_places,
    find_direct_bus_lines,
    direct_bus_routes,
    create_attraction_visit_plan,
)
from config.database import get_db

router = APIRouter()


@router.get("/nearest_places/", response_model=List[Place])
async def nearest_places_route(
    lat: float, long: float, db: AsyncSession = Depends(get_db)
):
    try:
        return await nearest_places(db, lat, long)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/nearest_restrooms/", response_model=List[Place])
async def nearest_restrooms_route(
    lat: float, long: float, db: AsyncSession = Depends(get_db)
):
    try:
        return await nearest_restrooms(db, lat, long)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/direct_bus_routes/", response_model=Dict[str, Any])
async def direct_bus_routes_route(
    lat1: float,
    long1: float,
    lat2: float,
    long2: float,
    buffer_radius: float = 0.5,
    db: AsyncSession = Depends(get_db),
):
    """
    Get the best direct bus route between two locations.
    Returns details about the optimal bus line and stops.
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
    lat: float,
    long: float,
    max_places: int = 5,
    visit_duration_hours: float | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a suggested plan for visiting nearby attractions.
    Returns an itinerary with timing and attraction details.
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
