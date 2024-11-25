# server/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, User
from config.database import get_db
from services.user_service import create_user, get_user, delete_user, update_user

router = APIRouter()


@router.post("/users/", response_model=User, status_code=201)
async def create_user_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_user(db, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/users/{user_id}", response_model=User)
async def read_user_route(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/users/{user_id}", status_code=204)
async def delete_user_route(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Attempt to delete the user
        success = await delete_user(db, user_id)
        if not success:
            # If deletion is unsuccessful (e.g., user not found), raise a 404 error
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        # Handle any other exceptions that might occur
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user: " + str(e)
        )


@router.put("/users/{user_id}", response_model=User)
async def update_user_route(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Update the user and return the updated record
        updated_user = await update_user(db, user_id, user)
        if not updated_user:
            # If no user was updated, raise a 404 error
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except Exception as e:
        # Catch and handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user: " + str(e)
        )
