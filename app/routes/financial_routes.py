from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.financial_record import RecordCreate, RecordResponse, RecordUpdate
from app.schemas.user import UserRole
from app.services.financial_service import (
    create_record,
    get_records,
    update_record,
    delete_record,
)
from app.core.dependencies import require_roles

router = APIRouter(prefix="/records", tags=["Financial Records"])


# Create → Admin only
@router.post(
    "/",
    response_model=RecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create financial record (Admin only)",
)
def create_record_api(
    record: RecordCreate,
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles([UserRole.admin])),
):
    # since no auth system
    user_id = 1
    return create_record(db, record, user_id)


# Read → All roles
@router.get(
    "/",
    response_model=list[RecordResponse],
    status_code=status.HTTP_200_OK,
    summary="Get financial records",
)
def get_records_api(
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles(list(UserRole))),
):
    user_id = 1
    return get_records(db, user_id)


# Update → Admin only
@router.put(
    "/{record_id}",
    response_model=RecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update financial record (Admin only)",
)
def update_record_api(
    record_id: int,
    record: RecordUpdate,
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles([UserRole.admin])),
):
    return update_record(db, record_id, record)


# Delete → Admin only
@router.delete(
    "/{record_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete financial record (Admin only)",
)
def delete_record_api(
    record_id: int,
    db: Session = Depends(get_db),
    role: UserRole = Depends(require_roles([UserRole.admin])),
):
    return delete_record(db, record_id)
