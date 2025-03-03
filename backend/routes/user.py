from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend.authentication.encryption import hash_password
from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.auth_dependencies import require_role
from backend.dependencies.db_dependencies import get_db
from backend.models.user import User
from backend.schemas.authentication import TokenData
from backend.schemas.user import UserResponse, UserUpdateRequest
from backend.utils.user_utils import email_exists, get_user_by_id

user_router = APIRouter(prefix="/user", tags=['User'])

class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int ) -> UserResponse:
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        return UserResponse.model_validate(user.model_dump())

    def get_users(self) -> list[UserResponse]:
        users = self.db.exec(select(User)).all()
        return [UserResponse.model_validate(user.model_dump()) for user in users]

    def update_user(self, user_id: int, user_update: UserUpdateRequest ) -> UserResponse:
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        if user_update.email and user_update.email != user.email:
            if email_exists(email=user_update.email, db=self.db):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            user.email = user_update.email

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "password":
                setattr(user, "hashed_password", hash_password(password=key))
            elif hasattr(user, key):
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

        return UserResponse.model_validate(user.model_dump())

    # when user gets deleted all their links with boards gets deleted ( UserBoardLink class )
    def delete_user(self, user_id: int) :
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        self.db.delete(user)
        self.db.commit()
        return None

def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)

@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int,
             controller: UserController = Depends(get_user_controller),
             _: TokenData = Depends(get_current_user),
             __: TokenData = Depends(require_role(["admin"]))
             ):
    return controller.get_user(user_id=user_id)

@user_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users( controller: UserController = Depends(get_user_controller),
              _: TokenData = Depends(get_current_user),
              __: TokenData = Depends(require_role(["admin"]))
              ):
    return controller.get_users()

@user_router.patch("/update/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int,
                user_update: UserUpdateRequest,
                controller: UserController = Depends(get_user_controller),
                _: TokenData = Depends(get_current_user),
                __: TokenData = Depends(require_role(["admin"]))
                ):
    return controller.update_user(user_id=user_id, user_update=user_update)

@user_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,
                controller: UserController = Depends(get_user_controller),
                _: TokenData = Depends(get_current_user),
                __: TokenData = Depends(require_role(["admin"]))
                ):
    return controller.delete_user(user_id=user_id)
