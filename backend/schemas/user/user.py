from pydantic import BaseModel

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str

class UserUpdateRequest(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

