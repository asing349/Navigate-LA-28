# server/services/review_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, ReviewUpdate

async def create_review(db: AsyncSession, review: ReviewCreate) -> ReviewModel:
    db_review = ReviewModel(**review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_review(db: AsyncSession, review_id: int) -> ReviewModel:
    result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
    return result.scalars().first()

async def update_review(db: AsyncSession, review_id: int, review: ReviewUpdate) -> ReviewModel:
    result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
    db_review = result.scalars().first()
    if db_review:
        update_data = review.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)
        await db.commit()
        await db.refresh(db_review)
        return db_review
    return None

async def delete_review(db: AsyncSession, review_id: int) -> bool:
    result = await db.execute(select(ReviewModel).filter(ReviewModel.id == review_id))
    db_review = result.scalars().first()
    if db_review:
        await db.delete(db_review)
        await db.commit()
        return True
    return False
