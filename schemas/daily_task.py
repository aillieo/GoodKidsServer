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
