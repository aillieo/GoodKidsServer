from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a sqlite engine instance
engine = create_engine("sqlite:///gk.db")

# Create a DeclarativeMeta instance
_Base = declarative_base()


class Base(_Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


# Create SessionLocal class from sessionmaker factory
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
