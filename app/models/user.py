from sqlalchemy import Column, Integer, String, Enum, DateTime
from database import Base
from sqlalchemy.orm import relationship
from enums import UserType
from datetime import datetime

# Define User class inheriting from Base


class User(Base):
    __tablename__ = 'users'
    username = Column(String)
    password = Column(String)
    avatar = Column(String)
    user_type = Column(Enum(UserType))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    daily_tasks = relationship('DailyTask', back_populates='user')
    user_items = relationship('UserItem', back_populates='user')
