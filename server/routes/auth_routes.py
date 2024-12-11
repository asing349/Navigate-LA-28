# server/routes/auth_routes.py

# Import FastAPI modules for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
# For asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta  # For calculating token expiration times
# For handling login form data
from fastapi.security import OAuth2PasswordRequestForm

# Import schemas and database utilities
# User schema for authentication (not used in this file but part of auth flow)
from schemas.user import UserAuth
from config.database import get_db  # Dependency for obtaining a database session

# Import authentication services and configurations
from services.auth_service import (
    authenticate_user,  # Service function to authenticate users
    create_access_token,  # Service function to generate access tokens
    ACCESS_TOKEN_EXPIRE_MINUTES,  # Configuration for token expiration time
)
from schemas.token import Token  # Schema for the token response

# Create a router instance for authentication routes
router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    # Form data dependency for extracting login credentials
    form_data: OAuth2PasswordRequestForm = Depends(),
    # Dependency for obtaining the database session
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint for user login and access token generation.

    Args:
        form_data (OAuth2PasswordRequestForm): Extracts username and password from the form data.
        db (AsyncSession): Database session for querying the user table.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If authentication fails (401 Unauthorized) or an unexpected error occurs (500 Internal Server Error).
    """
    try:
        # Attempt to authenticate the user with the provided credentials
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            # If authentication fails, raise a 401 Unauthorized error
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                # Error message for failed authentication
                detail="Incorrect username or password",
                # Header indicating the type of authentication required
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Calculate the token expiration time
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Generate a JWT access token
        access_token = create_access_token(
            # Include the username in the token's payload
            data={"sub": user.username},
            expires_delta=access_token_expires,  # Set the token's expiration duration
        )

        # Return the generated token and its type
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as e:
        # Rethrow HTTP exceptions without modification
        raise e

    except Exception as e:
        # Catch all other unexpected errors and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),  # Include the error details for debugging
            # Header indicating the type of authentication required
            headers={"WWW-Authenticate": "Bearer"},
        )
