from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.user import UserCreate, UserResponse, UserRole, UserUpdate
from app.services.user_service import (
    create_user,
    get_users,
    update_user,
    toggle_user_status,
)
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


# only can admins can update user info
@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user_api(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles([UserRole.admin])),
):
    return update_user(db, user_id, user_data)


# Toggle active/inactive
@router.patch(
    "/{user_id}/toggle-status",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def toggle_status_api(
    user_id: int,
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles([UserRole.admin])),
):
    return toggle_user_status(db, user_id)
