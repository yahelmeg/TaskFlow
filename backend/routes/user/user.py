from fastapi import APIRouter, Depends, HTTPException, status
from backend.models.user import User
from sqlmodel import Session, select
from backend.database.db_dependencies import get_db
from backend.schemas.user.user import UserCreateRequest, UserResponse, UserUpdateRequest
from backend.database.db_utils import db_add_and_refresh
from backend.authentication.encryption import hash_password
from user_utils import email_exists, username_exists, get_user_by_id

router = APIRouter()
user_router = APIRouter(prefix="/user")

@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    # todo : check permission

    if username_exists(username=user.username,db=db ):
        raise HTTPException(status_code=400, detail="Username already taken")
    if email_exists(email= user.email, db= db):
        raise HTTPException(status_code=400, detail="Email already taken")

    hashed_password = hash_password(password=user.password)
    new_user = db_add_and_refresh(db=db, obj=User(username=user.username, email=user.email, hashed_password=hashed_password))
    return new_user

@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # todo : check permission

    user = get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    # todo : check permission

    users = db.exec(select(User)).all()
    return users


@user_router.put("/update/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_update: UserUpdateRequest, db: Session = Depends(get_db)):
    # todo : check permission
    user = get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username and user_update.username != user.username:
        if username_exists(username=user_update.username, db=db):
            raise HTTPException(status_code=400, detail="Username already taken")

    if user_update.email and user_update.email != user.email:
        if email_exists(email=user_update.email, db=db):
            raise HTTPException(status_code=400, detail="Email already registered")

    user.username = user_update.username
    user.email = user_update.email
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(user)

    return user


@user_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # todo : check permission
    user = get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return None

