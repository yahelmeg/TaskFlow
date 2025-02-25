from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from backend.models.user import User
from backend.database.db_dependencies import get_db
from backend.schemas.user import UserResponse
from backend.schemas.authentication import CreateRequest, LoginRequest, Token
from backend.database.db_utils import db_add_and_refresh
from backend.authentication.encryption import hash_password
from backend.utils.user_utils import email_exists, get_user_by_email
from backend.authentication.encryption import verify_password
from backend.authentication.jwt_handler import create_access_token, create_refresh_token, get_current_user

auth_router = APIRouter(prefix="", tags=['Authentication'])

class AuthController:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: CreateRequest, active_user: User = Depends(get_current_user)) -> UserResponse:
        #todo check permissions
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

        if db_user.roles:
            permissions = list({perm.name for role in db_user.roles for perm in role.permissions})
        else:
            permissions = []

        access_token = create_access_token({"sub": str(db_user.id), "permissions": permissions})
        refresh_token = create_refresh_token({"sub": db_user.id})


        return Token(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")


@auth_router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateRequest, db: Session = Depends(get_db), active_user: User = Depends(get_current_user)):
    return AuthController(db).create_user(user,active_user)

@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    return AuthController(db).login(user_credentials)

@auth_router.post("/logout")
def logout():
    # todo revoke refresh tokens
    return {"message": "Logged out successfully."}

@auth_router.post("/refresh")
def refresh_access_token():
    # todo refresh access token using refresh token
    return {"message": "Token Refreshed."}
