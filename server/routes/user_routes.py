# server/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.user import UserCreate, User
from ..config.database import get_db
from ..services.user_services import create_user, get_user, delete_user, update_user

router = APIRouter()

@router.post("/users/", response_model=User, status_code=201)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=User)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=204)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
def update_user_route(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
