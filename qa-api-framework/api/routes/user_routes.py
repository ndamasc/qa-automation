from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db.session import get_db

from api.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from api.services import user_service
from api.db.session import SessionLocal

router = APIRouter(prefix="/users", tags=["users"])


        
@router.post("/", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, user.name, user.email, user.password)

    if not user:
        raise HTTPException(status_code=409, detail="Email already exists")
    return user


@router.get("/", response_model=list[UserResponse])
def list_all(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

#user_routes.py
@router.patch("/{user_id}", response_model=UserResponse)
def patch(user_id:int, user_data: UserUpdate, db:Session = Depends(get_db)):
    user = user_service.update_user(db, user_id, name=user_data.name, email=user_data.email, password=user_data.password)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    user = user_service.delete_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "deleted"}