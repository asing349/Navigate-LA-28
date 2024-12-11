# server/routes/analytics_routes.py

# APIRouter for defining routes; Query for request query parameters
from fastapi import APIRouter, Query
from typing import Optional  # For optional query parameters
# Service layer for analytics operations
from services.analytics_service import analytics_service

# Create an APIRouter instance for analytics routes
router = APIRouter()


@router.get("/attractions")
async def get_top_attractions(
    # Minimum rating filter (optional, range 0–5)
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    category: Optional[str] = None,  # Category filter (optional)
    # Limit for the number of results (default 10, range 1–100)
    limit: int = Query(10, ge=1, le=100),
):
    """
    Endpoint to retrieve the top-rated attractions.

    Args:
        min_rating (float, optional): Minimum rating to filter attractions (0–5).
        category (str, optional): Category of attractions to filter by.
        limit (int): Maximum number of attractions to return (default: 10).

    Returns:
        JSON: A list of the top-rated attractions based on the provided filters.
    """
    analytics = analytics_service  # Retrieve the analytics service instance
    # Call the service method
    return await analytics.get_top_attractions(min_rating, category, limit)


@router.get("/demographics")
async def get_demographics():
    """
    Endpoint to retrieve user demographics data.

    Returns:
        JSON: A summary of user demographics, such as age groups and geographic distribution.
    """
    analytics = analytics_service  # Retrieve the analytics service instance
    return await analytics.get_user_demographics()  # Call the service method


@router.get("/bus-routes")
async def get_bus_routes(
    # Minimum number of trips filter (optional, >= 0)
    min_trips: Optional[int] = Query(None, ge=0),
    # Limit for the number of results (default 10, range 1–100)
    limit: int = Query(10, ge=1, le=100),
):
    """
    Endpoint to retrieve analytics on bus routes.

    Args:
        min_trips (int, optional): Minimum number of trips to filter bus routes (>= 0).
        limit (int): Maximum number of bus routes to return (default: 10).

    Returns:
        JSON: A list of bus routes and their analytics based on the provided filters.
    """
    analytics = analytics_service  # Retrieve the analytics service instance
    # Call the service method
    return await analytics.get_bus_routes_analysis(min_trips, limit)


@router.get("/popular-stops")
async def get_popular_stops(
    # Minimum usage filter (optional, >= 0)
    min_usage: Optional[int] = Query(None, ge=0),
    line: Optional[str] = None,  # Bus line filter (optional)
    # Limit for the number of results (default 10, range 1–100)
    limit: int = Query(10, ge=1, le=100),
):
    """
    Endpoint to retrieve the most popular bus stops.

    Args:
        min_usage (int, optional): Minimum number of usages to filter stops (>= 0).
        line (str, optional): Bus line to filter stops by.
        limit (int): Maximum number of bus stops to return (default: 10).

    Returns:
        JSON: A list of popular bus stops based on the provided filters.
    """
    analytics = analytics_service  # Retrieve the analytics service instance
    # Call the service method
    return await analytics.get_popular_stops(min_usage, line, limit)


@router.get("/geographic-distribution")
async def get_geographic_distribution():
    """
    Endpoint to retrieve the geographic distribution of user activities.

    Returns:
        JSON: Geographic data representing the distribution of user activities.
    """
    analytics = analytics_service  # Retrieve the analytics service instance
    return await analytics.get_geographic_distribution()  # Call the service method
