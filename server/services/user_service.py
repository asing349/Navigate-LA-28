# server/services/user_service.py

# Asynchronous database session management
from sqlalchemy.ext.asyncio import AsyncSession
# SQLAlchemy future for constructing queries
from sqlalchemy.future import select
# Exception handling for SQLAlchemy errors
from sqlalchemy.exc import SQLAlchemyError
# Enables eager loading of relationships
from sqlalchemy.orm import selectinload
import bcrypt  # Library for hashing passwords securely
from typing import Optional  # For optional return types

from models.user import User as UserModel  # Import the User model
from schemas.user import UserCreate  # Import Pydantic schema for user creation


async def create_user(db: AsyncSession, user: UserCreate) -> UserModel:
    """
    Create a new user in the database.

    Args:
        db (AsyncSession): Asynchronous database session.
        user (UserCreate): Schema containing user creation data.

    Returns:
        UserModel: The newly created user object with relationships.

    Raises:
        Exception: If an error occurs during the creation process.
    """
    try:
        # Hash the user's password
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        )
        # Create a new user instance
        db_user = UserModel(
            username=user.username,
            # Convert hashed password to string
            password=hashed_password.decode("utf-8"),
            dob=user.dob,
            country=user.country,
            reviews=[],  # Initialize reviews relationship as empty
            usages=[],  # Initialize usages relationship as empty
        )
        db.add(db_user)  # Add user to the database session
        await db.commit()  # Commit the transaction

        # Fetch the created user with relationships loaded
        stmt = (
            select(UserModel)
            .filter(UserModel.id == db_user.id)
            .options(selectinload(UserModel.reviews), selectinload(UserModel.usages))
        )
        result = await db.execute(stmt)  # Execute the query
        return result.scalars().first()  # Return the user object
    except SQLAlchemyError as e:
        await db.rollback()  # Rollback in case of an error
        raise Exception(f"Error creating user: {str(e)}")


async def get_user(db: AsyncSession, user_id: int) -> Optional[UserModel]:
    """
    Retrieve a user by their ID.

    Args:
        db (AsyncSession): Asynchronous database session.
        user_id (int): ID of the user to retrieve.

    Returns:
        Optional[UserModel]: The user object if found, otherwise None.

    Raises:
        Exception: If an error occurs during retrieval.
    """
    try:
        # Query the database for the user with the given ID
        result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalars().first()  # Get the first matching user or None
        if user:
            await db.refresh(user)  # Refresh to explicitly load relationships
        return user
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching user: {str(e)}")


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    Delete a user from the database.

    Args:
        db (AsyncSession): Asynchronous database session.
        user_id (int): ID of the user to delete.

    Returns:
        bool: True if the user was deleted, False if not found.

    Raises:
        Exception: If an error occurs during deletion.
    """
    try:
        # Retrieve the user to delete
        result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = result.scalars().first()
        if db_user:
            await db.delete(db_user)  # Mark the user for deletion
            await db.commit()  # Commit the transaction
            return True
        return False  # User not found
    except SQLAlchemyError as e:
        await db.rollback()  # Rollback in case of an error
        raise Exception(f"Error deleting user: {str(e)}")


async def update_user(
    db: AsyncSession, user_id: int, user_update: UserCreate
) -> Optional[UserModel]:
    """
    Update an existing user's details.

    Args:
        db (AsyncSession): Asynchronous database session.
        user_id (int): ID of the user to update.
        user_update (UserCreate): Schema containing updated user data.

    Returns:
        Optional[UserModel]: The updated user object if successful, otherwise None.

    Raises:
        Exception: If an error occurs during the update process.
    """
    try:
        # Retrieve the user to update
        result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = result.scalars().first()
        if db_user:
            # Update user fields
            db_user.username = user_update.username
            db_user.dob = user_update.dob
            db_user.country = user_update.country
            # Hash and update the password
            db_user.password = bcrypt.hashpw(
                user_update.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            await db.commit()  # Commit the transaction
            await db.refresh(db_user)  # Refresh to get updated state
            return db_user
        return None  # User not found
    except SQLAlchemyError as e:
        await db.rollback()  # Rollback in case of an error
        raise Exception(f"Error updating user: {str(e)}")
