from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base


class CompletionRecord(Base):
    __tablename__ = 'completionrecords'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    note = Column(String(256))

    task_id = Column(Integer, ForeignKey('dailytasks.id'))
    task = relationship("DailyTask", back_populates="completion_records")
