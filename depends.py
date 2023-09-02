from typing import List
from fastapi import FastAPI, Depends
from database import Base, engine, SessionLocal

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
