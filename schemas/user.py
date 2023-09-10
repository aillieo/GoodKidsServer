from typing import Optional
from pydantic import BaseModel
# Base User Schema (Pydantic Model)


class UserBase(BaseModel):
    username: str

# Create User Schema (Pydantic Model)


class UserCreate(UserBase):
    password: str


# Update User Schema (Pydantic Model)
class UserUpdate(UserBase):
    password: str

# Complete User Schema (Pydantic Model)


class User(UserBase):
    id: int
    password: str

    class Config:
        orm_mode = True
