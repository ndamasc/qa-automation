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


def update_user(db, user_id, name=None, email=None, password=None):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    if email:
        email_exists = (
            db.query(User)
            .filter(User.email == email, User.id != user_id)
            .first()
        )

        if email_exists:
            raise ValueError("Email already exists")

        user.email = email

    if name:
        user.name = name

    if password:
        user.password = hash_password(password)

    db.commit()
    db.refresh(user)

    return user


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


# def _safe_hash(password: str) -> str:
#     print("PASSWORD RECEBIDO:", password)
#     print("TIPO:", type(password))
#     print("BYTES:", len(password.encode("utf-8")))

#     if not password:
#         raise ValueError("Password cannot be empty")
    
#     if len(password.encode("utf-8")) > 72:
#         raise ValueError("Password too long")

#     password_bytes = password.encode("utf-8")[:72]
    
#     return pwd_context.hash(password_bytes)



def _safe_hash(password: str) -> str:

    if not password:
        raise ValueError("Password cannot be empty")

    # 🔥 corta em bytes corretamente
    password_bytes = password.encode("utf-8")[:72]

    # 🔥 volta pra string antes de passar pro passlib
    safe_password = password_bytes.decode("utf-8", errors="ignore")

    return pwd_context.hash(safe_password)

#####






def hash_password(password: str) -> str:
    return _safe_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)