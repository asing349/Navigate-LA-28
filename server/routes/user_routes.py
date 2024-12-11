# server/routes/user_routes.py

# Import FastAPI modules for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
# For handling asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import schemas for request and response validation
from schemas.user import UserCreate, User
# Import database dependency for session management
from config.database import get_db
# Import service functions for user operations
from services.user_service import create_user, get_user, delete_user, update_user

# Create an APIRouter instance for user routes
router = APIRouter()


@router.post("/users/", response_model=User, status_code=201)
async def create_user_route(
    user: UserCreate,  # Request body containing user data to create
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to create a new user.

    Args:
        user (UserCreate): The user data to create.
        db (AsyncSession): Database session for executing queries.

    Returns:
        User: The newly created user.

    Raises:
        HTTPException: If there is an error during user creation (400 Bad Request).
    """
    try:
        # Call the service function to create the user
        return await create_user(db, user)
    except Exception as e:
        # Handle errors and return a 400 Bad Request with the error details
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/users/{user_id}", response_model=User)
async def read_user_route(
    user_id: int,  # ID of the user to retrieve
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (AsyncSession): Database session for executing queries.

    Returns:
        User: The retrieved user.

    Raises:
        HTTPException:
            - 404 Not Found: If the user is not found.
    """
    # Retrieve the user by ID
    user = await get_user(db, user_id)
    if not user:
        # If no user is found, raise a 404 Not Found error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",  # Error message for missing user
        )
    return user  # Return the retrieved user


@router.delete("/users/{user_id}", status_code=204)
async def delete_user_route(
    user_id: int,  # ID of the user to delete
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (AsyncSession): Database session for executing queries.

    Returns:
        None: A successful deletion returns a 204 No Content response.

    Raises:
        HTTPException:
            - 404 Not Found: If the user is not found.
            - 500 Internal Server Error: For unexpected errors.
    """
    try:
        # Attempt to delete the user
        success = await delete_user(db, user_id)
        if not success:
            # If no user is deleted, raise a 404 Not Found error
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",  # Error message for missing user
            )
    except Exception as e:
        # Handle unexpected exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # Include error details for debugging
            detail="Failed to delete user: " + str(e),
        )


@router.put("/users/{user_id}", response_model=User)
async def update_user_route(
    user_id: int,  # ID of the user to update
    user: UserCreate,  # Request body containing updated user data
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to update a user by their ID.

    Args:
        user_id (int): The ID of the user to update.
        user (UserCreate): The updated user data.
        db (AsyncSession): Database session for executing queries.

    Returns:
        User: The updated user.

    Raises:
        HTTPException:
            - 404 Not Found: If the user is not found.
            - 500 Internal Server Error: For unexpected errors.
    """
    try:
        # Update the user and return the updated record
        updated_user = await update_user(db, user_id, user)
        if not updated_user:
            # If no user is updated, raise a 404 Not Found error
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",  # Error message for missing user
            )
        return updated_user  # Return the updated user
    except Exception as e:
        # Handle unexpected exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # Include error details for debugging
            detail="Failed to update user: " + str(e),
        )
