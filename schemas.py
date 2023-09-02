from pydantic import BaseModel

# Base DailyTask Schema (Pydantic Model)
class DailyTaskBase(BaseModel):
    taskName: str
    taskDes: str

# Create DailyTask Schema (Pydantic Model)
class DailyTaskCreate(DailyTaskBase):
    pass

# Update DailyTask Schema (Pydantic Model)
class DailyTaskUpdate(DailyTaskBase):
    pass

# Complete DailyTask Schema (Pydantic Model)
class DailyTask(DailyTaskBase):
    id: int

    class Config:
        orm_mode = True

# Base User Schema (Pydantic Model)
class UserBase(BaseModel):
    name: str
    password: str

# Create User Schema (Pydantic Model)
class UserCreate(UserBase):
    pass

# Update User Schema (Pydantic Model)
class UserUpdate(UserBase):
    pass

# Complete User Schema (Pydantic Model)
class User(UserBase):
    id: int

    class Config:
        orm_mode = True

