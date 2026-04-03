from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import date
from app.models.financial_record import FinancialRecord
from app.schemas.financial_record import RecordCreate, RecordUpdate, RecordType


# Create record
def create_record(db: Session, data: RecordCreate, user_id: int):

    # duplicate check
    existing_record = (
        db.query(FinancialRecord)
        .filter(
            FinancialRecord.user_id == user_id,
            FinancialRecord.amount == data.amount,
            FinancialRecord.type == data.type,
            FinancialRecord.category.ilike(data.category),  # case-insensitive
            FinancialRecord.date == data.date,
        )
        .first()
    )

    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate record already exists",
        )

    try:
        record = FinancialRecord(
            amount=data.amount,
            type=data.type,
            category=data.category,
            date=data.date,
            notes=data.notes,
            user_id=user_id,
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating record",
        )


# Get records (no filters)
def get_records(db: Session, user_id: int):
    return (
        db.query(FinancialRecord)
        .filter(FinancialRecord.user_id == user_id)
        .order_by(FinancialRecord.date.desc())
        .all()
    )


# Update record
def update_record(db: Session, record_id: int, data: RecordUpdate, user_id: int):

    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found",
        )

    # ownership check
    if record.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this record",
        )

    try:
        # partial update
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(record, key, value)

        db.commit()
        db.refresh(record)
        return record

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating record",
        )


# Delete record
def delete_record(db: Session, record_id: int, user_id: int):

    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found",
        )

    # ownership check
    if record.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this record",
        )

    try:
        db.delete(record)
        db.commit()
        return {"detail": "Record deleted successfully"}

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while deleting record",
        )


# Filter records
def get_filtered_records(
    db: Session,
    user_id: int,
    type: Optional[RecordType] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):

    # base query
    query = db.query(FinancialRecord).filter(FinancialRecord.user_id == user_id)

    # invalid date range
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date",
        )

    # filters
    if type:
        query = query.filter(FinancialRecord.type == type)

    if category:
        query = query.filter(
            FinancialRecord.category.ilike(category)  # case-insensitive
        )

    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)

    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)

    # sorting (latest first)
    return query.order_by(
        FinancialRecord.date.desc(),
        FinancialRecord.id.desc(),
    ).all()
