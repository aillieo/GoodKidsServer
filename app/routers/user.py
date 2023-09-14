from fastapi import APIRouter, Request, HTTPException, security
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import depends

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()


@router.get("/{id}", response_model=schemas.User)
def read_user(id: int, session: Session = Depends(depends.get_session)):

    # get the user item with the given id
    user = session.query(models.User).get(id)

    # check if user item with given id exists. If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")

    return user


@router.put("/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.UserUpdate, session: Session = Depends(depends.get_session)):

    # get the user item with the given id
    user_db = session.query(models.User).get(id)

    # update user item with the given user (if an item with the given id was found)
    if user_db:
        user_db.name = user.name
        user_db.password = user.password
        session.commit()

    # check if user item with given id exists. If not, raise exception and return 404 not found response
    if not user_db:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")

    return user_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(depends.get_session)):

    # get the user item with the given id
    user = session.query(models.User).get(id)

    # if daily task item with given id exists, delete it from the database. Otherwise raise 404 error
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")

    return None


@router.get("/", response_model=List[schemas.User])
def read_user_list(session: Session = Depends(depends.get_session)):

    # get all user items
    user_list = session.query(models.User).all()

    return user_list
