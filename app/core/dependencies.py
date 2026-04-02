from fastapi import Header, HTTPException, status
from app.schemas.user import UserRole


def get_current_role(x_role: str = Header(...)):
    """
    Simulating authentication using headers
    Example: x-role: admin
    """

    try:
        role = UserRole(x_role)  # convert string → Enum
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role provided"
        )

    return role


def require_roles(allowed_roles: list[UserRole]):
    def role_checker(x_role: str = Header(...)):
        try:
            role = UserRole(x_role)  # convert string → Enum
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role provided"
            )

        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        return role

    return role_checker
