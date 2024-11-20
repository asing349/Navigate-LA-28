# server/services/user_service.py
from sqlalchemy.orm import Session
import bcrypt

from models.user import User as UserModel
from schemas.user import UserCreate

def create_user(db: Session, user: UserCreate) -> UserModel:
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = UserModel(username=user.username, password=hashed_password.decode('utf-8'), dob=user.dob, country=user.country)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, user_update: UserCreate) -> UserModel:
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        db_user.username = user_update.username
        db_user.dob = user_update.dob
        db_user.country = user_update.country
        db_user.password = bcrypt.hashpw(user_update.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.commit()
        db.refresh(db_user)
        return db_user
    return None
