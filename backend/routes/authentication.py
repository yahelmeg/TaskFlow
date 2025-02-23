from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from backend.models.user import User
from backend.database.db_dependencies import get_db
from backend.schemas.user import UserResponse
from backend.schemas.authentication import UserCreateRequest, UserLoginRequest
from backend.database.db_utils import db_add_and_refresh
from backend.authentication.encryption import hash_password
from backend.utils.user_utils import email_exists, username_exists, get_user_by_username, get_user_by_email
from backend.authentication.encryption import verify_password
from backend.authentication.jwt_handler import create_access_token, create_refresh_token

auth_router = APIRouter(prefix="")


class AuthController:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreateRequest) -> UserResponse:
        if username_exists(username=user.username, db=self.db):
            raise HTTPException(status_code=400, detail="Username already taken")
        if email_exists(email=user.email, db=self.db):
            raise HTTPException(status_code=400, detail="Email already taken")

        hashed_password = hash_password(password=user.password)
        new_user = db_add_and_refresh(
            db=self.db,
            obj=User(username=user.username, email=user.email, hashed_password=hashed_password)
        )
        return new_user

    def login(self, user: UserLoginRequest):
        if not user.username and not user.email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        db_user = None
        if user.username:
            db_user = get_user_by_username(user.username, self.db)
        if not db_user and user.email:
            db_user = get_user_by_email(user.email, self.db)

        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = create_access_token({"sub": db_user.username})
        refresh_token = create_refresh_token({"sub": db_user.username})

        return {"access_token": access_token, "refresh_token": refresh_token}

@auth_router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    return AuthController(db).create_user(user)

@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
    return AuthController(db).login(user)