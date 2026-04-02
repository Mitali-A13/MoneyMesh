from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import date
from app.models.financial_record import FinancialRecord
from app.schemas.financial_record import RecordCreate, RecordUpdate
from app.schemas.financial_record import RecordType


# Create record
def create_record(db: Session, data: RecordCreate, user_id: int):

    # duplicate check
    existing_record = (
        db.query(FinancialRecord)
        .filter(
            FinancialRecord.user_id == user_id,
            FinancialRecord.amount == data.amount,
            FinancialRecord.type == data.type,
            FinancialRecord.category == data.category,
            FinancialRecord.date == data.date,
        )
        .first()
    )

    if existing_record:
        raise HTTPException(status_code=409, detail="Duplicate record already exists")

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
            status_code=500, detail="Something went wrong while creating record"
        )


# Get records (user specific)
def get_records(db: Session, user_id: int):
    return db.query(FinancialRecord).filter(FinancialRecord.user_id == user_id).all()


# Update record
def update_record(db: Session, record_id: int, data: RecordUpdate):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
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
def delete_record(db: Session, record_id: int):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
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


# Filtering records
def get_filtered_records(
    db: Session,
    user_id: int,
    type: Optional[RecordType] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    # user-specific data
    query = db.query(FinancialRecord).filter(FinancialRecord.user_id == user_id)

    # filters
    if type:
        query = query.filter(FinancialRecord.type == type)

    if category:
        query = query.filter(FinancialRecord.category == category)

    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)

    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)

    # for invalid date range
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date",
        )

    return query.all()
