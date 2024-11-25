# server/services/customer_usage_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from models.customer_usage import CustomerUsage as CustomerUsageModel
from schemas.customer_usage import CustomerUsageCreate


async def create_customer_usage(db: AsyncSession, customer_usage: CustomerUsageCreate, user_id: int) -> CustomerUsageModel:
    try:
        # Create a new customer usage record
        db_customer_usage = CustomerUsageModel(
            **customer_usage.dict(), user_id=user_id)
        db.add(db_customer_usage)
        await db.commit()  # Commit changes to the database
        await db.refresh(db_customer_usage)  # Refresh to get the updated state
        return db_customer_usage
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        raise Exception(f"Error creating customer usage: {str(e)}")


async def get_customer_usage(db: AsyncSession, customer_usage_id: int) -> CustomerUsageModel:
    try:
        # Retrieve customer usage by ID
        result = await db.execute(select(CustomerUsageModel).filter(CustomerUsageModel.id == customer_usage_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy-specific errors
        raise Exception(f"Error fetching customer usage: {str(e)}")
