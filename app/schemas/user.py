from pydantic import BaseModel, Field
from typing import Annotated, Optional
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"


# reusable types
NameType = Annotated[
    str, Field(..., min_length=2, max_length=50, description="User name")
]
RoleType = Annotated[
    UserRole, Field(..., description="User role (admin, analyst, viewer)")
]
IdType = Annotated[int, Field(..., description="User ID")]
IsActiveType = Annotated[bool, Field(default=True, description="User active status")]


class UserCreate(BaseModel):
    name: NameType
    role: RoleType


class UserUpdate(BaseModel):
    name: Optional[NameType] = None
    role: Optional[RoleType] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: IdType
    name: NameType
    role: RoleType
    is_active: IsActiveType

    class Config:
        from_attributes = True
