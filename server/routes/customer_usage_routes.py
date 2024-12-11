# server/routes/customer_usage_routes.py

# Import necessary FastAPI modules for routing, dependencies, and exceptions
from fastapi import APIRouter, Depends, HTTPException, status
# For handling asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession

# Import schemas for request and response validation
from schemas.customer_usage import CustomerUsageCreate, CustomerUsage
# Import service functions for customer usage operations
from services.customer_usage_service import create_customer_usage, get_customer_usage
# Import database dependency for session management
from config.database import get_db

# Create an APIRouter instance for customer usage routes
router = APIRouter()


@router.post("/customer-usage/", response_model=CustomerUsage, status_code=201)
async def create_customer_usage_route(
    # Request body containing customer usage data
    customer_usage: CustomerUsageCreate,
    user_id: int,  # ID of the user associated with the usage data
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to create a new customer usage record.

    Args:
        customer_usage (CustomerUsageCreate): The customer usage data to be created.
        user_id (int): The ID of the user associated with the usage record.
        db (AsyncSession): Database session for executing queries.

    Returns:
        CustomerUsage: The newly created customer usage record.

    Raises:
        HTTPException: If an unexpected error occurs during creation (500 Internal Server Error).
    """
    try:
        # Create customer usage data and return the newly created record
        return await create_customer_usage(db, customer_usage, user_id)
    except Exception as e:
        # Handle any unexpected exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),  # Include the error message for debugging
        )


@router.get("/customer-usage/{customer_usage_id}", response_model=CustomerUsage)
async def read_customer_usage_route(
    customer_usage_id: int,  # ID of the customer usage record to retrieve
    db: AsyncSession = Depends(get_db),  # Database session dependency
):
    """
    Endpoint to retrieve a customer usage record by its ID.

    Args:
        customer_usage_id (int): The ID of the customer usage record to retrieve.
        db (AsyncSession): Database session for executing queries.

    Returns:
        CustomerUsage: The retrieved customer usage record.

    Raises:
        HTTPException:
            - 404 Not Found: If the record does not exist.
            - 500 Internal Server Error: For unexpected errors.
    """
    try:
        # Retrieve customer usage data by its ID
        customer_usage = await get_customer_usage(db, customer_usage_id)
        if not customer_usage:
            # If the record is not found, return a 404 Not Found error
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer usage not found",  # Error message for missing data
            )
        return customer_usage  # Return the retrieved record
    except HTTPException as e:
        # Rethrow known HTTP exceptions for FastAPI to handle
        raise e
    except Exception as e:
        # Handle unexpected exceptions and return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),  # Include the error message for debugging
        )
