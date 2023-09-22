from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class TaskItem(Base):
    __tablename__ = 'taskitems'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('dailytasks.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer, default=0)
    task = relationship('DailyTask', back_populates='task_items')
    item = relationship('Item')
