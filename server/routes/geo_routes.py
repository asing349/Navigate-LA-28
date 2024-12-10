from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas.review import ReviewCreate, Review, ReviewUpdate
from schemas.place import Place
from services.geo_service import nearest_restrooms, nearest_places
from config.database import get_db

router = APIRouter()


@router.get("/nearest_places/", response_model=List[Place])
async def nearest_places_route(
    lat: float, long: float, db: AsyncSession = Depends(get_db)
):
    try:
        print(f"Received coordinates: lat={lat}, long={long}")
        return await nearest_places(db, lat, long)
    except Exception as e:
        print(f"Error: {e}")
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
