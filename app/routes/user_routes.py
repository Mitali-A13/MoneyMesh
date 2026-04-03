from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.user import UserResponse, UserRole, UserUpdate
from app.services.user_service import (
    get_users,
    update_user,
    toggle_user_status,
)
from app.core.dependencies import require_roles
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


# all users can view users
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(list(UserRole))),
):
    return get_users(db)


# only admins can update user
@router.put("/{user_id}", response_model=UserResponse)
def update_user_api(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.admin])),
):
    return update_user(db, user_id, user_data)


# toggle active/inactive
@router.patch("/{user_id}/toggle-status", response_model=UserResponse)
def toggle_status_api(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.admin])),
):
    return toggle_user_status(db, user_id)
