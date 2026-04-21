from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.db.session import get_db

from api.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from api.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

        
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    user_obj = user_service.create_user(db, user.name, user.email, user.password)

    if not user_obj:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return user_obj


@router.get("/", response_model=list[UserResponse])
def list_all(db: Session = Depends(get_db)):
    """List all users."""
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    user = user_service.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


# user_routes.py

@router.patch("/{user_id}", response_model=UserResponse)
def patch(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Update a user partially."""

    try:
        user = user_service.update_user(
            db,
            user_id,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    success = user_service.delete_user(db, user_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")