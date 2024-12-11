# server/services/review_service.py

# Import for asynchronous database session management
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import to construct SQL queries
# Import for handling SQLAlchemy-specific errors
from sqlalchemy.exc import SQLAlchemyError

from models.review import Review as ReviewModel  # Import the Review model
# Import Pydantic schemas for review creation and updates
from schemas.review import ReviewCreate, ReviewUpdate


async def create_review(db: AsyncSession, review: ReviewCreate) -> ReviewModel:
    """
    Create a new review record in the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        review (ReviewCreate): The Pydantic schema for creating a new review.

    Returns:
        ReviewModel: The newly created review object.

    Raises:
        Exception: If an error occurs during the creation process.
    """
    try:
        # Create a new review instance using data from the schema
        db_review = ReviewModel(**review.dict())
        db.add(db_review)  # Add the review to the database session
        await db.commit()  # Commit the transaction to save changes
        # Refresh the instance to retrieve updated state
        await db.refresh(db_review)
        return db_review
    except SQLAlchemyError as e:
        # Rollback the transaction in case of an error
        await db.rollback()
        raise Exception(f"Error creating review: {str(e)}")


async def get_review(db: AsyncSession, review_id: int) -> ReviewModel:
    """
    Retrieve a review record by its ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        review_id (int): The unique identifier of the review.

    Returns:
        ReviewModel: The retrieved review object, or None if not found.

    Raises:
        Exception: If an error occurs during retrieval.
    """
    try:
        # Query the database to find the review with the specified ID
        result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
        return result.scalars().first()  # Return the first matching record or None
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching review: {str(e)}")


async def update_review(db: AsyncSession, review_id: int, review: ReviewUpdate) -> ReviewModel:
    """
    Update an existing review record with new data.

    Args:
        db (AsyncSession): The asynchronous database session.
        review_id (int): The unique identifier of the review to update.
        review (ReviewUpdate): The Pydantic schema with updated review data.

    Returns:
        ReviewModel: The updated review object, or None if not found.

    Raises:
        Exception: If an error occurs during the update process.
    """
    try:
        # Query the database to find the review with the specified ID
        result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
        db_review = result.scalars().first()
        if db_review:
            # Update the fields provided in the schema
            update_data = review.dict(
                exclude_unset=True)  # Exclude unset fields
            for key, value in update_data.items():
                # Update the attributes of the review
                setattr(db_review, key, value)
            await db.commit()  # Commit the transaction to save changes
            # Refresh the instance to retrieve updated state
            await db.refresh(db_review)
            return db_review
        return None  # Return None if the review is not found
    except SQLAlchemyError as e:
        # Rollback the transaction in case of an error
        await db.rollback()
        raise Exception(f"Error updating review: {str(e)}")


async def delete_review(db: AsyncSession, review_id: int) -> bool:
    """
    Delete a review record from the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        review_id (int): The unique identifier of the review to delete.

    Returns:
        bool: True if the review was deleted successfully, False if not found.

    Raises:
        Exception: If an error occurs during the deletion process.
    """
    try:
        # Query the database to find the review with the specified ID
        result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
        db_review = result.scalars().first()
        if db_review:
            await db.delete(db_review)  # Mark the review for deletion
            await db.commit()  # Commit the transaction to save changes
            return True  # Return True to indicate successful deletion
        return False  # Return False if the review is not found
    except SQLAlchemyError as e:
        # Rollback the transaction in case of an error
        await db.rollback()
        raise Exception(f"Error deleting review: {str(e)}")
