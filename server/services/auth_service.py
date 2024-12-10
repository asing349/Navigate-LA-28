# server/services/auth_service.py
from datetime import datetime, timedelta, timezone
import os
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User as UserModel

SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with your secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    try:
        result = await db.execute(select(UserModel).filter(UserModel.username == username))
        user = result.scalars().first()
        if user and verify_password(password, user.password):
            return user
        return None
    except Exception as e:
        # Log error details, handle or re-raise as appropriate
        # Here, we choose to simply re-raise an error for simplicity
        raise RuntimeError(f"Authentication failed: {str(e)}")

def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Default to 15 minutes if no delta provided
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError as e:
        # Handle errors from JWT encoding
        raise JWTError(f"Failed to create access token: {str(e)}")
