from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

# Define DailyTask class inheriting from Base


class DailyTask(Base):
    __tablename__ = 'dailytasks'
    id = Column(Integer, primary_key=True)
    taskName = Column(String(256))
    taskDes = Column(String(256))
    create_time = Column(DateTime, default=datetime.now)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='daily_tasks')

    completion_records = relationship('CompletionRecord', back_populates='task')
