# server/services/customer_usage_service.py
from sqlalchemy.orm import Session

from models.customer_usage import CustomerUsage as CustomerUsageModel
from schemas.customer_usage import CustomerUsageCreate

def create_customer_usage(db: Session, customer_usage: CustomerUsageCreate, user_id: int) -> CustomerUsageModel:
    db_customer_usage = CustomerUsageModel(**customer_usage.dict(), user_id=user_id)
    db.add(db_customer_usage)
    db.commit()
    db.refresh(db_customer_usage)
    return db_customer_usage

def get_customer_usage(db: Session, customer_usage_id: int) -> CustomerUsageModel:
    return db.query(CustomerUsageModel).filter(CustomerUsageModel.id == customer_usage_id).first()
