from pydantic import BaseModel, Field
from typing import Annotated
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


class UserCreate(BaseModel):
    name: NameType
    role: RoleType


class UserResponse(BaseModel):
    id: IdType
    name: NameType
    role: RoleType
    is_active: bool

    class Config:
        from_attributes = True
