from pydantic import BaseModel, model_validator
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class CreateRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

