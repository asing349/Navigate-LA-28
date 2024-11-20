# server/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import bcrypt
from typing import Optional
from models.user import User as UserModel
from schemas.user import UserCreate


async def create_user(db: AsyncSession, user: UserCreate) -> UserModel:
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = UserModel(
        username=user.username,
        password=hashed_password.decode("utf-8"),
        dob=user.dob,
        country=user.country,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int) -> UserModel:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    return result.scalars().first()


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False


async def update_user(
    db: AsyncSession, user_id: int, user_update: UserCreate
) -> Optional[UserModel]:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        db_user.username = user_update.username
        db_user.dob = user_update.dob
        db_user.country = user_update.country
        db_user.password = bcrypt.hashpw(
            user_update.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        await db.commit()
        await db.refresh(db_user)
        return db_user
    return None
