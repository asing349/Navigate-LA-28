# server/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
import bcrypt
from typing import Optional

from models.user import User as UserModel
from schemas.user import UserCreate


async def create_user(db: AsyncSession, user: UserCreate) -> UserModel:
    try:
        # Hash the user's password before storing it in the database
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        db_user = UserModel(
            username=user.username,
            password=hashed_password.decode("utf-8"),
            dob=user.dob,
            country=user.country,
            reviews=[],  # Initialize empty relationships
            usages=[],
        )
        db.add(db_user)
        await db.commit()  # Commit the transaction

        # Fetch the complete user with relationships after creation
        stmt = (
            select(UserModel)
            .filter(UserModel.id == db_user.id)
            .options(selectinload(UserModel.reviews), selectinload(UserModel.usages))
        )
        result = await db.execute(stmt)
        return result.scalars().first()
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        raise Exception(f"Error creating user: {str(e)}")


async def get_user(db: AsyncSession, user_id: int) -> Optional[UserModel]:
    try:
        # Retrieve user by ID
        result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching user: {str(e)}")


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    try:
        # Retrieve the user to delete
        result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = result.scalars().first()
        if db_user:
            await db.delete(db_user)  # Mark the user for deletion
            await db.commit()  # Commit the transaction
            return True
        return False
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        raise Exception(f"Error deleting user: {str(e)}")


async def update_user(
    db: AsyncSession, user_id: int, user_update: UserCreate
) -> Optional[UserModel]:
    try:
        # Retrieve the user to update
        result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = result.scalars().first()
        if db_user:
            # Update user fields
            db_user.username = user_update.username
            db_user.dob = user_update.dob
            db_user.country = user_update.country
            db_user.password = bcrypt.hashpw(
                user_update.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            await db.commit()  # Commit the transaction
            await db.refresh(db_user)  # Refresh to get the updated state
            return db_user
        return None
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        raise Exception(f"Error updating user: {str(e)}")
