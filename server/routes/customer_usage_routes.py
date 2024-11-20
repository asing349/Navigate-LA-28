# server/routes/customer_usage_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.customer_usage import CustomerUsageCreate, CustomerUsage
from services.customer_usage_service import create_customer_usage, get_customer_usage
from config.database import get_db

router = APIRouter()

@router.post("/customer-usage/", response_model=CustomerUsage, status_code=201)
def create_customer_usage_route(customer_usage: CustomerUsageCreate, user_id: int, db: Session = Depends(get_db)):
    return create_customer_usage(db, customer_usage, user_id)

@router.get("/customer-usage/{customer_usage_id}", response_model=CustomerUsage)
def read_customer_usage_route(customer_usage_id: int, db: Session = Depends(get_db)):
    customer_usage = get_customer_usage(db, customer_usage_id)
    if not customer_usage:
        raise HTTPException(status_code=404, detail="Customer usage not found")
    return customer_usage
