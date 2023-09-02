from fastapi import APIRouter, Cookie, Request, HTTPException
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


@router.post("/dailytask", response_model=schemas.DailyTask, status_code=status.HTTP_201_CREATED)
async def create_daily_task(daily_task: schemas.DailyTaskCreate, session: Session = Depends(depends.get_session)):

    # create an instance of the dailytask database model
    daily_task_db = models.DailyTask(
        taskName=daily_task.taskName, taskDes=daily_task.taskDes)

    # add it to the session and commit it
    session.add(daily_task_db)
    session.commit()
    session.refresh(daily_task_db)

    # return the daily task object
    return daily_task_db


@router.get("/dailytask/{id}", response_model=schemas.DailyTask)
def read_daily_task(id: int, session: Session = Depends(depends.get_session)):

    # get the daily task item with the given id
    daily_task = session.query(models.DailyTask).get(id)

    # check if daily task item with given id exists. If not, raise exception and return 404 not found response
    if not daily_task:
        raise HTTPException(
            status_code=404, detail=f"daily task item with id {id} not found")

    return daily_task


@router.put("/dailytask/{id}", response_model=schemas.DailyTask)
def update_daily_task(id: int, daily_task: schemas.DailyTaskUpdate, session: Session = Depends(depends.get_session)):

    # get the daily task item with the given id
    daily_task_db = session.query(models.DailyTask).get(id)

    # update daily task item with the given task (if an item with the given id was found)
    if daily_task_db:
        daily_task.taskName = daily_task.taskName
        daily_task.taskDes = daily_task.taskDes
        session.commit()

    # check if daily task item with given id exists. If not, raise exception and return 404 not found response
    if not daily_task_db:
        raise HTTPException(
            status_code=404, detail=f"daily task item with id {id} not found")

    return daily_task_db


@router.delete("/dailytask/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_task(id: int, session: Session = Depends(depends.get_session)):

    # get the daily task item with the given id
    daily_task = session.query(models.DailyTask).get(id)

    # if daily task item with given id exists, delete it from the database. Otherwise raise 404 error
    if daily_task:
        session.delete(daily_task)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"dailytask item with id {id} not found")

    return None


@router.get("/dailytask", response_model=List[schemas.DailyTask])
def read_daily_task_list(user: int = Cookie(None), session: Session = Depends(depends.get_session)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # get all daily task items
    daily_task_list = session.query(models.DailyTask).all()

    return daily_task_list
