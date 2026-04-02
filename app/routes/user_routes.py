from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.user import UserCreate, UserResponse, UserRole
from app.services.user_service import create_user, get_users
from app.core.dependencies import require_roles

router = APIRouter(prefix="/users", tags=["Users"])


# only admins can create users
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_api(
    user: UserCreate,
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles([UserRole.admin])),
):
    return create_user(db, user.name, user.role)


# all users can view the users
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users_api(
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles(list(UserRole))),
):
    return get_users(db)
