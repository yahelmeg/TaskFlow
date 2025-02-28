from fastapi import APIRouter, HTTPException, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import UTC, datetime

from backend.authentication.encryption import hash_password, verify_password
from backend.authentication.jwt_handler import create_access_token, create_refresh_token, verify_token
from backend.dependencies.db_dependencies import get_db
from backend.models.user import User
from backend.schemas.authentication import RegisterRequest, Token
from backend.schemas.user import UserResponse
from backend.utils.db_utils import db_add_and_refresh
from backend.utils.user_utils import email_exists, get_user_by_email, get_user_by_id
from backend.utils.token_utils import blacklist_refresh_token, check_blacklisted


auth_router = APIRouter(prefix="", tags=['Authentication'])

class AuthController:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user: RegisterRequest) -> UserResponse:
        if email_exists(email=user.email, db=self.db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken")

        hashed_password = hash_password(password=user.password)
        new_user = db_add_and_refresh(
            db=self.db,
            obj=User( email=user.email, name=user.name, hashed_password=hashed_password)
        )
        return new_user

    def login(self, user_credentials: OAuth2PasswordRequestForm = Depends() ) -> Token:

        db_user = get_user_by_email(user_credentials.username, self.db)

        if not db_user or not verify_password(user_credentials.password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        roles = [role.name for role in db_user.roles] if db_user.roles else []

        access_token = create_access_token({"sub": str(db_user.id), "roles": roles})
        refresh_token = create_refresh_token({"sub": str(db_user.id)})

        return Token(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")

    def refresh_token(self, refresh_token: str) -> Token:
        print("here")
        payload = verify_token(token=refresh_token, exception_message="Invalid refresh token" )
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        db_user = get_user_by_id(user_id=user_id, db=self.db)

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        roles = [role.name for role in db_user.roles] if db_user.roles else []

        if check_blacklisted(token=refresh_token, db=self.db):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted")

        expires_at = datetime.fromtimestamp(payload["exp"], tz=UTC)
        blacklist_refresh_token(token=refresh_token, expires_at=expires_at, db=self.db)

        new_access_token = create_access_token({"sub": str(db_user.id), "roles": roles})
        new_refresh_token = create_refresh_token({"sub": str(db_user.id)})

        return Token(access_token=new_access_token, refresh_token=new_refresh_token, token_type="Bearer")

    def logout(self, refresh_token: str):

        payload = verify_token(token=refresh_token, exception_message="Invalid refresh token")
        expires_at = datetime.fromtimestamp(payload["exp"], tz=UTC)
        blacklist_refresh_token(token=refresh_token, expires_at=expires_at, db=self.db)

        return {"message": "Logged out successfully."}


def get_authentication_controller(db: Session = Depends(get_db)) -> AuthController:
    return AuthController(db)

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: RegisterRequest, controller: AuthController = Depends(get_authentication_controller)):
    return controller.register(user)

@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,
          controller: AuthController = Depends(get_authentication_controller)):
    return controller.login(user_credentials)

@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(refresh_token: str = Body(..., embed=True),
            controller: AuthController = Depends(get_authentication_controller)):
    return controller.refresh_token(refresh_token=refresh_token)

@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(refresh_token: str = Body(..., embed=True),
           controller: AuthController = Depends(get_authentication_controller)):
    return controller.logout(refresh_token=refresh_token)


