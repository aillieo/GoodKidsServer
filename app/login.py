from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from typing import List
from fastapi import status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import depends
import models
import schemas
import security

router = APIRouter()


@router.post("/register", response_model=schemas.Token)
async def register(user_create: schemas.Login, session: Session = Depends(depends.get_session)) -> schemas.Token:
    user_db = session.query(models.User).filter(
        models.User.username == user_create.username).first()

    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this name already exist"
        )

    user_db = models.User(
        username=user_create.username,
        password=security.get_hashed_password(user_create.password)
    )

    # add it to the session and commit it
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    token = schemas.Token(
        token=security.create_token(str(user_db.id)),
        uid=user_db.id)
    return token


@router.post("/login", response_model=schemas.Token)
async def login(user_create: schemas.Login, session: Session = Depends(depends.get_session)) -> schemas.Token:

    user_db = session.query(models.User).filter(
        models.User.username == user_create.username).first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"user not exist")

    if not security.verify_password(user_create.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect password"
        )

    token = schemas.Token(
        token=security.create_token(str(user_db.id)),
        uid=user_db.id)
    return token


@router.get("/me", response_model=schemas.User)
def get_me(
        user: models.User = Depends(depends.get_current_user)) -> models.User:
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user
