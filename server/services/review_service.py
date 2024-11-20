# server/services/review_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, ReviewUpdate

async def create_review(db: AsyncSession, review: ReviewCreate) -> ReviewModel:
    try:
        # Create a new review record
        db_review = ReviewModel(**review.dict())
        db.add(db_review)
        await db.commit()  # Commit changes to the database
        await db.refresh(db_review)  # Refresh to get the updated state
        return db_review
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        raise Exception(f"Error creating review: {str(e)}")

async def get_review(db: AsyncSession, review_id: int) -> ReviewModel:
    try:
        # Retrieve review by ID
        result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy-specific errors
        raise Exception(f"Error fetching review: {str(e)}")

async def update_review(db: AsyncSession, review_id: int, review: ReviewUpdate) -> ReviewModel:
    try:
        # Retrieve the existing review record
        result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
        db_review = result.scalars().first()
        if db_review:
            # Update only the provided fields
            update_data = review.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_review, key, value)
            await db.commit()
            await db.refresh(db_review)
            return db_review
        return None
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        raise Exception(f"Error updating review: {str(e)}")

async def delete_review(db: AsyncSession, review_id: int) -> bool:
    try:
        # Retrieve the review record to delete
        result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
        db_review = result.scalars().first()
        if db_review:
            await db.delete(db_review)  # Mark the record for deletion
            await db.commit()  # Commit the deletion
            return True
        return False
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        raise Exception(f"Error deleting review: {str(e)}")
