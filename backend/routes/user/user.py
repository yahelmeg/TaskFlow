from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from backend.models.user import User
from backend.database.db_dependencies import get_db
from backend.schemas.user.user import UserCreateRequest, UserResponse, UserUpdateRequest
from backend.database.db_utils import db_add_and_refresh
from backend.authentication.encryption import hash_password
from backend.utils.user_utils import email_exists, username_exists, get_user_by_id

router = APIRouter()
user_router = APIRouter(prefix="/user")

class UserController:
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

    def get_user(self, user_id: int) -> UserResponse:
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

    def get_users(self) -> list[UserResponse]:
        users = self.db.exec(select(User)).all()
        return [UserResponse.model_validate(user) for user in users]

    def update_user(self, user_id: int, user_update: UserUpdateRequest) -> UserResponse:
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user_update.username and user_update.username != user.username:
            if username_exists(username=user_update.username, db=self.db):
                raise HTTPException(status_code=400, detail="Username already taken")

        if user_update.email and user_update.email != user.email:
            if email_exists(email=user_update.email, db=self.db):
                raise HTTPException(status_code=400, detail="Email already registered")

        user.username = user_update.username
        user.email = user_update.email
        if user_update.password:
            user.hashed_password = hash_password(user_update.password)

        self.db.commit()
        self.db.refresh(user)

        return UserResponse.model_validate(user)

    def delete_user(self, user_id: int):
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.db.delete(user)
        self.db.commit()

        return None

# Use the controller in your routes
@user_router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    return UserController(db).create_user(user)

@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserController(db).get_user(user_id)

@user_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    return UserController(db).get_users()

@user_router.put("/update/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_update: UserUpdateRequest, db: Session = Depends(get_db)):
    return UserController(db).update_user(user_id, user_update)

@user_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserController(db).delete_user(user_id)
