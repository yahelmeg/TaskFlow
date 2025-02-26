from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from backend.models.user import User
from backend.database.db_dependencies import get_db
from backend.schemas.user import UserResponse, UserUpdateRequest
from backend.authentication.encryption import hash_password
from backend.utils.user_utils import email_exists,get_user_by_id
from backend.authentication.jwt_handler import get_current_user, require_role
from backend.schemas.authentication import TokenData


user_router = APIRouter(prefix="/user", tags=['User'])

class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int, active_user: TokenData ) -> UserResponse:
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user.model_dump())

    def get_users(self, active_user: TokenData) -> list[UserResponse]:
        users = self.db.exec(select(User)).all()
        return [UserResponse.model_validate(user.model_dump()) for user in users]

    def update_user(self, user_id: int, user_update: UserUpdateRequest, active_user: TokenData ) -> UserResponse:
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user_update.email and user_update.email != user.email:
            if email_exists(email=user_update.email, db=self.db):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            user.email = user_update.email

        if user_update.name:
            user.name = user_update.name

        if user_update.password:
            user.hashed_password = hash_password(user_update.password)

        self.db.commit()
        self.db.refresh(user)

        return UserResponse.model_validate(user.model_dump())

    def delete_user(self, user_id: int, active_user: TokenData):
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        self.db.delete(user)
        self.db.commit()

        return None

@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int,
             db: Session = Depends(get_db),
             active_user: TokenData = Depends(get_current_user),
             _: TokenData = Depends(require_role(["admin"]))
             ):
    return UserController(db).get_user(user_id, active_user)

@user_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db),
              active_user: TokenData = Depends(get_current_user),
              _: TokenData = Depends(require_role(["admin"]))
              ):
    return UserController(db).get_users(active_user)

@user_router.patch("/update/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int,
                user_update: UserUpdateRequest,
                db: Session = Depends(get_db),
                active_user: TokenData = Depends(get_current_user),
                _: TokenData = Depends(require_role(["admin"]))
                ):
    return UserController(db).update_user(user_id, user_update, active_user)

@user_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                active_user: TokenData = Depends(get_current_user),
                _: TokenData = Depends(require_role(["admin"]))
                ):
    return UserController(db).delete_user(user_id, active_user)
