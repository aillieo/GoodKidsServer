from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class UserItem(Base):
    __tablename__ = 'useritems'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer, default=0)
    user = relationship('User', back_populates='user_items')
    item = relationship('Item')
