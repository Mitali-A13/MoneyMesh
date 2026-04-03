from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# Register API
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register_api(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(
        db=db,
        name=user.name,
        email=user.email,
        role=user.role,
        password=user.password,
    )


# Login API
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login user and return JWT token",
)
def login_api(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=user.email,
        password=user.password,
    )
