# server/routes/review_routes.py

# Import FastAPI modules for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
# For asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import schemas for request and response validation
from schemas.review import ReviewCreate, Review, ReviewUpdate
# Import service functions for review operations
from services.review_service import create_review, get_review, update_review, delete_review
# Import database dependency for session management
from config.database import get_db

# Create an APIRouter instance for review routes
router = APIRouter()

# Define a constant for the "Review not found" message
REVIEW_NOT_FOUND = "Review not found"


@router.post("/reviews/", response_model=Review, status_code=201)
async def create_review_route(
    review: ReviewCreate,  # Request body containing review data
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to create a new review.

    Args:
        review (ReviewCreate): The review data to be created.
        db (AsyncSession): Database session for executing queries.

    Returns:
        Review: The newly created review.

    Raises:
        HTTPException: If an unexpected error occurs during creation (500 Internal Server Error).
    """
    try:
        # Create a new review and return the created record
        return await create_review(db, review)
    except Exception as e:
        # Handle unexpected errors and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),  # Include the error details for debugging
        )


@router.get("/reviews/{review_id}", response_model=Review)
async def read_review_route(
    review_id: int,  # ID of the review to retrieve
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to retrieve a review by its ID.

    Args:
        review_id (int): The ID of the review to retrieve.
        db (AsyncSession): Database session for executing queries.

    Returns:
        Review: The retrieved review.

    Raises:
        HTTPException:
            - 404 Not Found: If the review is not found.
            - 500 Internal Server Error: For unexpected errors.
    """
    try:
        # Retrieve the review by ID
        review = await get_review(db, review_id)
        if not review:
            detail = REVIEW_NOT_FOUND,  # Error message for missing review
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,  # Error message for missing review
            )
        return review  # Return the retrieved review
    except HTTPException as e:
        # Rethrow known HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),  # Include the error details for debugging
        )


@router.put("/reviews/{review_id}", response_model=Review)
async def update_review_route(
    review_id: int,  # ID of the review to update
    review: ReviewUpdate,  # Request body containing updated review data
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to update a review by its ID.

    Args:
        review_id (int): The ID of the review to update.
        review (ReviewUpdate): The updated review data.
        db (AsyncSession): Database session for executing queries.

    Returns:
        Review: The updated review.

    Raises:
        HTTPException:
            - 404 Not Found: If the review is not found.
            - 500 Internal Server Error: For unexpected errors.
    """
    try:
        # Update the review and return the updated record
        updated_review = await update_review(db, review_id, review)
        if not updated_review:
            # If no review is updated, raise a 404 Not Found error
            detail = REVIEW_NOT_FOUND,  # Error message for missing review
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,  # Error message for missing review
            )
        return updated_review  # Return the updated review
    except HTTPException as e:
        # Rethrow known HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),  # Include the error details for debugging
        )


@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review_route(
    review_id: int,  # ID of the review to delete
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to delete a review by its ID.

    Args:
        review_id (int): The ID of the review to delete.
        db (AsyncSession): Database session for executing queries.

    Returns:
        None: A successful deletion returns a 204 No Content response.

    Raises:
        HTTPException:
            - 404 Not Found: If the review is not found.
            - 500 Internal Server Error: For unexpected errors.
    """
    try:
        # Attempt to delete the review
        if not await delete_review(db, review_id):
            # If no review is deleted, raise a 404 Not Found error
            detail = REVIEW_NOT_FOUND,  # Error message for missing review
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,  # Error message for missing review
            )
    except HTTPException as e:
        # Rethrow known HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),  # Include the error details for debugging
        )
