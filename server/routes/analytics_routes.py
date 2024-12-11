from fastapi import APIRouter, Query
from typing import Optional
from services.analytics_service import analytics_service

router = APIRouter()


@router.get("/attractions")
async def get_top_attractions(
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    category: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
):
    analytics = analytics_service
    return await analytics.get_top_attractions(min_rating, category, limit)


@router.get("/demographics")
async def get_demographics():
    analytics = analytics_service
    return await analytics.get_user_demographics()


@router.get("/bus-routes")
async def get_bus_routes(
    min_trips: Optional[int] = Query(None, ge=0), limit: int = Query(10, ge=1, le=100)
):
    analytics = analytics_service
    return await analytics.get_bus_routes_analysis(min_trips, limit)


@router.get("/popular-stops")
async def get_popular_stops(
    min_usage: Optional[int] = Query(None, ge=0),
    line: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
):
    analytics = analytics_service
    return await analytics.get_popular_stops(min_usage, line, limit)


@router.get("/geographic-distribution")
async def get_geographic_distribution():
    analytics = analytics_service
    return await analytics.get_geographic_distribution()
