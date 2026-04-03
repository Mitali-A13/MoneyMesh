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

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# Summary
@router.get(
    "/summary",
    status_code=status.HTTP_200_OK,
    summary="Get financial summary (income, expense, balance)",
)
def summary_api(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(list(UserRole))),
):
    return get_summary(db, user["id"])


# Category breakdown
@router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    summary="Get category-wise expense/income breakdown",
)
def category_api(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(list(UserRole))),
):
    return get_category_breakdown(db, user["id"])


# Recent activity
@router.get(
    "/recent",
    status_code=status.HTTP_200_OK,
    summary="Get last 5 financial records",
)
def recent_api(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(list(UserRole))),
):
    return get_recent_activity(db, user["id"])


# Monthly trends
@router.get(
    "/trends",
    status_code=status.HTTP_200_OK,
    summary="Get month-wise financial trends",
)
def trends_api(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(list(UserRole))),
):
    return get_monthly_trends(db, user["id"])
