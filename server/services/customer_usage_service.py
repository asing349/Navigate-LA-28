# server/services/customer_usage_service.py

# For asynchronous database session management
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # For constructing SQL queries
# For handling SQLAlchemy-specific errors
from sqlalchemy.exc import SQLAlchemyError

# CustomerUsage model from the database
from models.customer_usage import CustomerUsage as CustomerUsageModel
# Schema for creating a new CustomerUsage record
from schemas.customer_usage import CustomerUsageCreate


async def create_customer_usage(db: AsyncSession, customer_usage: CustomerUsageCreate, user_id: int) -> CustomerUsageModel:
    """
    Create a new customer usage record.

    Args:
        db (AsyncSession): The asynchronous database session.
        customer_usage (CustomerUsageCreate): The data for creating a new customer usage record.
        user_id (int): The ID of the user associated with the customer usage.

    Returns:
        CustomerUsageModel: The newly created customer usage record.

    Raises:
        Exception: If an error occurs during the creation process.
    """
    try:
        # Initialize a new CustomerUsageModel instance with the provided data
        db_customer_usage = CustomerUsageModel(
            **customer_usage.dict(), user_id=user_id)
        db.add(db_customer_usage)  # Add the new record to the database session
        await db.commit()  # Commit changes to the database
        # Refresh the instance to include changes from the database
        await db.refresh(db_customer_usage)
        return db_customer_usage
    except SQLAlchemyError as e:
        # Rollback changes in case of an error
        await db.rollback()
        raise Exception(f"Error creating customer usage: {str(e)}")


async def get_customer_usage(db: AsyncSession, customer_usage_id: int) -> CustomerUsageModel:
    """
    Retrieve a customer usage record by its ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        customer_usage_id (int): The ID of the customer usage record to retrieve.

    Returns:
        CustomerUsageModel: The retrieved customer usage record, or None if not found.

    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    try:
        # Execute a query to retrieve the customer usage record by its ID
        result = await db.execute(select(CustomerUsageModel).filter(CustomerUsageModel.id == customer_usage_id))
        return result.scalars().first()  # Return the first result or None if not found
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-specific errors
        raise Exception(f"Error fetching customer usage: {str(e)}")
