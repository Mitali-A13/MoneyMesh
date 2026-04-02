from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserRole


def create_user(db: Session, name: str, role: UserRole):
    # existing user check
    existing_user = db.query(User).filter(User.name == name).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this name already exists",
        )

    try:
        user = User(name=name, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating user",
        )


def get_users(db: Session):
    return db.query(User).all()
