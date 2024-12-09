from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.review import ReviewCreate, Review, ReviewUpdate
from services.geo_service import nearest_restrooms, nearest_places
from config.database import get_db

router = APIRouter()


@router.post("/nearest_places/", response_model=Review, status_code=201)
async def nearest_places_route(
    lat: float, long: float, db: AsyncSession = Depends(get_db)
):
    try:
        # Attempt to create a new review and return it
        return await nearest_places(db, lat, long)
    except Exception as e:
        # Handle any exceptions that occur during creation
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/nearest_restrooms/", response_model=Review, status_code=201)
async def nearest_restrooms(
    lat: float, long: float, db: AsyncSession = Depends(get_db)
):
    try:
        # Attempt to create a new review and return it
        return await nearest_restrooms(db, lat, long)
    except Exception as e:
        # Handle any exceptions that occur during creation
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
