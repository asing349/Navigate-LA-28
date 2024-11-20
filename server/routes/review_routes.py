# server/routes/review_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.review import ReviewCreate, Review, ReviewUpdate
from services.review_service import create_review, get_review, update_review, delete_review
from config.database import get_db

router = APIRouter()

@router.post("/reviews/", response_model=Review, status_code=201)
async def create_review_route(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Attempt to create a new review and return it
        return await create_review(db, review)
    except Exception as e:
        # Handle any exceptions that occur during creation
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/reviews/{review_id}", response_model=Review)
async def read_review_route(review_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Retrieve review by ID
        review = await get_review(db, review_id)
        if not review:
            # If the review is not found, raise a 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return review
    except HTTPException as e:
        # Rethrow the HTTPException to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch unexpected exceptions and return a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/reviews/{review_id}", response_model=Review)
async def update_review_route(review_id: int, review: ReviewUpdate, db: AsyncSession = Depends(get_db)):
    try:
        # Update the review and return the updated record
        updated_review = await update_review(db, review_id, review)
        if not updated_review:
            # If no review was updated, raise a 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return updated_review
    except HTTPException as e:
        # Rethrow the HTTPException
        raise e
    except Exception as e:
        # Catch and handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review_route(review_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Attempt to delete the review
        if not await delete_review(db, review_id):
            # If the deletion is unsuccessful (e.g., review not found), raise a 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    except HTTPException as e:
        # Rethrow the HTTPException
        raise e
    except Exception as e:
        # Handle any other exceptions that might occur
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
