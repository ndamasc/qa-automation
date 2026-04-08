from sqlalchemy.orm import Session
from api.db.models.user_model import User

def create_user(db:Session, name:str, email:str, password:str):
    user = User(name=name, email=email, password=password)
    
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db:Session):
    return db.query(User).all()

def update_user(db:Session, user_id:int, **kwargs):
    user = get_user(db, user_id)
    
    if not user:
        return False
    
    for field, value in kwargs.items():
        if value is not None:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


def get_user(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db:Session, user_id:int):
    user = get_user(db, user_id)
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    return True