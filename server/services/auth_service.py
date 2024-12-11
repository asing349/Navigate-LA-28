# server/services/auth_service.py

from datetime import datetime, timedelta, timezone  # For handling dates and times
import os  # For accessing environment variables
# For JSON Web Token (JWT) encoding and decoding
from jose import jwt, JWTError
# For password hashing and verification
from passlib.context import CryptContext
# For asynchronous database interactions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # For constructing SQL queries

from models.user import User as UserModel  # User model from the database

# Secret key and algorithm for JWT
SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with a secure key
ALGORITHM = "HS256"  # Hashing algorithm used for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash a plain text password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    Authenticate a user by verifying their username and password.

    Args:
        db (AsyncSession): The asynchronous database session.
        username (str): The username to authenticate.
        password (str): The plain text password to verify.

    Returns:
        UserModel: The authenticated user if credentials are valid, None otherwise.

    Raises:
        RuntimeError: If an error occurs during authentication.
    """
    try:
        # Query the database for the user with the given username
        result = await db.execute(select(UserModel).filter(UserModel.username == username))
        user = result.scalars().first()  # Fetch the first result
        if user and verify_password(password, user.password):  # Verify the password
            return user
        return None
    except Exception as e:
        # Handle any exceptions during authentication
        raise RuntimeError(f"Authentication failed: {str(e)}")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to include in the token's payload.
        expires_delta (timedelta, optional): The token's expiration time. Defaults to 15 minutes.

    Returns:
        str: The encoded JWT access token.

    Raises:
        JWTError: If an error occurs during token creation.
    """
    try:
        to_encode = data.copy()  # Copy the data to encode
        if expires_delta:
            # Use the provided expiration delta
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + \
                timedelta(minutes=15)  # Default to 15 minutes
        # Add the expiration time to the payload
        to_encode.update({"exp": expire})
        # Encode the JWT
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError as e:
        # Handle errors during token creation
        raise JWTError(f"Failed to create access token: {str(e)}")
