import jwt
from datetime import datetime, timedelta, UTC
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.schemas.authentication import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict) -> str :
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str :
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, exception_message: str) -> dict:
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_jwt
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception_message,
            headers={"WWW-Authenticate": "Bearer"}
        )

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData :
    payload = verify_token(token, "Authorization token is missing")
    user_id = payload.get("sub")
    user_permissions = payload.get("permissions")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenData(id=user_id, permissions=user_permissions)
