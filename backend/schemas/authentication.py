from pydantic import BaseModel

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    email: str
    password: str


