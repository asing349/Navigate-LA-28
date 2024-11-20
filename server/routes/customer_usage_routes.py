# server/routes/customer_usage_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.customer_usage import CustomerUsageCreate, CustomerUsage
from services.customer_usage_service import create_customer_usage, get_customer_usage
from config.database import get_db

router = APIRouter()

@router.post("/customer-usage/", response_model=CustomerUsage, status_code=201)
async def create_customer_usage_route(customer_usage: CustomerUsageCreate, user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Create customer usage data and return the newly created record
        return await create_customer_usage(db, customer_usage, user_id)
    except Exception as e:
        # Handle any exceptions that occur during creation
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/customer-usage/{customer_usage_id}", response_model=CustomerUsage)
async def read_customer_usage_route(customer_usage_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Retrieve customer usage data by ID
        customer_usage = await get_customer_usage(db, customer_usage_id)
        if not customer_usage:
            # If the data is not found, return a 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer usage not found")
        return customer_usage
    except HTTPException as e:
        # Rethrow the HTTPException to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch unexpected exceptions and return a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
