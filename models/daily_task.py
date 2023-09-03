from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Define DailyTask class inheriting from Base
class DailyTask(Base):
    __tablename__ = 'dailytasks'
    id = Column(Integer, primary_key=True)
    taskName = Column(String(256))
    taskDes = Column(String(256))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')
