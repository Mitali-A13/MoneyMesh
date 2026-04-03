from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.financial_record import FinancialRecord


# Total Income, Expense, Net Balance
def get_summary(db: Session, user_id: int):
    try:
        total_income = (
            db.query(func.coalesce(func.sum(FinancialRecord.amount), 0))
            .filter(
                FinancialRecord.user_id == user_id,
                FinancialRecord.type == "income",
            )
            .scalar()
        )

        total_expense = (
            db.query(func.coalesce(func.sum(FinancialRecord.amount), 0))
            .filter(
                FinancialRecord.user_id == user_id,
                FinancialRecord.type == "expense",
            )
            .scalar()
        )

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_balance": float(total_income - total_expense),
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching summary data",
        )


# Category-wise totals
def get_category_breakdown(db: Session, user_id: int):
    try:
        results = (
            db.query(
                FinancialRecord.category,
                func.coalesce(func.sum(FinancialRecord.amount), 0).label("total"),
            )
            .filter(FinancialRecord.user_id == user_id)
            .group_by(FinancialRecord.category)
            .order_by(func.sum(FinancialRecord.amount).desc())
            .all()
        )

        return [
            {
                "category": r.category,
                "total": float(r.total),
            }
            for r in results
        ]

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching category breakdown",
        )


# Recent activity (last 5 records)
def get_recent_activity(db: Session, user_id: int):
    try:
        records = (
            db.query(FinancialRecord)
            .filter(FinancialRecord.user_id == user_id)
            .order_by(
                FinancialRecord.date.desc(),
                FinancialRecord.id.desc(),  # tie-breaker 🔥
            )
            .limit(5)
            .all()
        )

        return records

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching recent activity",
        )


# Monthly trends
def get_monthly_trends(db: Session, user_id: int):
    try:
        results = (
            db.query(
                func.strftime("%Y-%m", FinancialRecord.date).label("month"),
                func.coalesce(func.sum(FinancialRecord.amount), 0).label("total"),
            )
            .filter(FinancialRecord.user_id == user_id)
            .group_by("month")
            .order_by("month")
            .all()
        )

        return [
            {
                "month": r.month,
                "total": float(r.total),
            }
            for r in results
        ]

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching monthly trends",
        )
