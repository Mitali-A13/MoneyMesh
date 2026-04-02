from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import date
from enum import Enum


# Enum for type (income/expense)
class RecordType(str, Enum):
    income = "income"
    expense = "expense"


# reusable types
AmountType = Annotated[float, Field(..., gt=0, description="Transaction amount")]

TypeType = Annotated[
    RecordType, Field(..., description="Type of record (income or expense)")
]

CategoryType = Annotated[
    str, Field(..., min_length=2, max_length=50, description="Transaction category")
]

DateType = Annotated[date, Field(..., description="Transaction date")]

NotesType = Annotated[
    Optional[str], Field(default=None, max_length=255, description="Optional notes")
]

IdType = Annotated[int, Field(..., description="Record ID")]

UserIdType = Annotated[int, Field(..., description="User ID associated with record")]


# Create schema
class RecordCreate(BaseModel):
    amount: AmountType
    type: TypeType
    category: CategoryType
    date: DateType
    notes: NotesType


# Update schema (partial update)
class RecordUpdate(BaseModel):
    amount: Optional[AmountType] = None
    type: Optional[TypeType] = None
    category: Optional[CategoryType] = None
    date: Optional[DateType] = None
    notes: Optional[str] = None


# Response schema
class RecordResponse(BaseModel):
    id: IdType
    amount: AmountType
    type: TypeType
    category: CategoryType
    date: DateType
    notes: NotesType
    user_id: UserIdType

    class Config:
        from_attributes = True
