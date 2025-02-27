from fastapi import Depends, HTTPException, status

from backend.authentication.jwt_handler import get_current_user
from backend.schemas.authentication import TokenData


def require_role(required_roles: list[str]):
    def role_checker(active_user: TokenData = Depends(get_current_user)):
        if not set(required_roles).issubset(set(active_user.roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not permitted",
            )
        return active_user
    return role_checker