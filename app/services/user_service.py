from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserRole, UserUpdate


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


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # existing name check
    if data.name:
        existing_user = db.query(User).filter(User.name == data.name).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this name already exists",
            )

    try:
        # partial update
        if data.name:
            user.name = data.name

        if data.role:
            user.role = data.role

        if data.is_active is not None:
            user.is_active = data.is_active

        db.commit()
        db.refresh(user)
        return user

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating user",
        )


def toggle_user_status(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        user.is_active = not user.is_active

        db.commit()
        db.refresh(user)
        return user

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating status",
        )
