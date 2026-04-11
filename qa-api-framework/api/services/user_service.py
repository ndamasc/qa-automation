from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from api.db.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, name: str, email: str, password: str) -> User | None:
    """Create a new user with hashed password and email uniqueness validation."""
    hashed_password = _safe_hash(password)
    user = User(name=name, email=email, password=hashed_password)
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None


def list_users(db: Session) -> list[User]:
    """List all users."""
    return db.query(User).all()


def update_user(db: Session, user_id: int, **kwargs) -> User | None:
    """Update user fields. Password will be hashed if provided."""
    user = get_user(db, user_id)
    
    if not user:
        return None
    
    for field, value in kwargs.items():
        if value is not None:
            if field == "password":
                value = _safe_hash(value)
            setattr(user, field, value)
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None


def get_user(db: Session, user_id: int) -> User | None:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user by ID."""
    user = get_user(db, user_id)
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    return True


def _safe_hash(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")

    pwd_bytes = password.encode("utf-8")[:72]
    safe_password = pwd_bytes.decode("utf-8", errors="ignore")

    return pwd_context.hash(safe_password)

def hash_password(password: str) -> str:
    return _safe_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)