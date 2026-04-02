from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_users

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.name, user.role)


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users_api(db: Session = Depends(get_db)):
    return get_users(db)
