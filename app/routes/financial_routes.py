from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.financial_record import (
    RecordCreate,
    RecordResponse,
    RecordUpdate,
    RecordType,
)
from app.schemas.user import UserRole
from app.services.financial_service import (
    create_record,
    update_record,
    delete_record,
    get_filtered_records,
)
from app.core.dependencies import require_roles

router = APIRouter(prefix="/records", tags=["Financial Records"])


# Create → Admin only
@router.post(
    "/",
    response_model=RecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_record_api(
    record: RecordCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([UserRole.admin])),
):

    return create_record(db, record, user["id"])


# GET + FILTER
@router.get(
    "/",
    response_model=list[RecordResponse],
    status_code=status.HTTP_200_OK,
)
def get_records_api(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(list(UserRole))),
    type: Optional[RecordType] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    return get_filtered_records(
        db=db,
        user_id=user["id"],
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date,
    )


# Update → Admin only
@router.put(
    "/{record_id}",
    response_model=RecordResponse,
)
def update_record_api(
    record_id: int,
    record: RecordUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([UserRole.admin])),
):
    return update_record(db, record_id, record, user["id"])


# Delete → Admin only
@router.delete("/{record_id}")
def delete_record_api(
    record_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([UserRole.admin])),
):
    return delete_record(db, record_id, user["id"])
