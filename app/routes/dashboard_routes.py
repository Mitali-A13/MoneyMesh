from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.dependencies import require_roles
from app.schemas.user import UserRole
from app.services.dashboard_service import (
    get_summary,
    get_category_breakdown,
    get_recent_activity,
    get_monthly_trends,
)
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# Summary
@router.get("/summary", status_code=status.HTTP_200_OK)
def summary_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(list(UserRole))),
):
    return get_summary(db, current_user.id)


# Category breakdown
@router.get("/categories", status_code=status.HTTP_200_OK)
def category_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(list(UserRole))),
):
    return get_category_breakdown(db, current_user.id)


# Recent activity
@router.get("/recent", status_code=status.HTTP_200_OK)
def recent_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(list(UserRole))),
):
    return get_recent_activity(db, current_user.id)


# Monthly trends
@router.get("/trends", status_code=status.HTTP_200_OK)
def trends_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(list(UserRole))),
):
    return get_monthly_trends(db, current_user.id)
