from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserRole
from app.core.security import hash_password, verify_password, create_access_token


# Register user
def register_user(db: Session, name: str, email: str, role: UserRole, password: str):

    # duplicate email check
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    try:
        user = User(
            name=name,
            email=email,
            role=role.value,
            hashed_password=hash_password(password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while registering user",
        )


# Login user
def login_user(db: Session, email: str, password: str):

    # find user
    user = db.query(User).filter(User.email == email).first()

    # invalid credentials
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # inactive user check
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    try:
        # create JWT token
        token = create_access_token(
            {
                "sub": str(user.id),  # standard field
                "role": user.role,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while generating token",
        )
