# server/services/customer_usage_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.customer_usage import CustomerUsage as CustomerUsageModel
from schemas.customer_usage import CustomerUsageCreate

async def create_customer_usage(db: AsyncSession, customer_usage: CustomerUsageCreate, user_id: int) -> CustomerUsageModel:
    db_customer_usage = CustomerUsageModel(**customer_usage.dict(), user_id=user_id)
    db.add(db_customer_usage)
    await db.commit()
    await db.refresh(db_customer_usage)
    return db_customer_usage

async def get_customer_usage(db: AsyncSession, customer_usage_id: int) -> CustomerUsageModel:
    result = await db.execute(select(CustomerUsageModel).filter(CustomerUsageModel.id == customer_usage_id))
    return result.scalars().first()
