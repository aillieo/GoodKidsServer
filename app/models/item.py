from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon = Column(String)
    tasks = relationship('TaskItem', back_populates='item')
    users = relationship('UserItem', back_populates='item')
