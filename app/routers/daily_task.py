from fastapi import APIRouter, Cookie, Request, HTTPException
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from crud import CRUD
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
from schema_utils import SchemaUtils
import schemas
import depends

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()


@router.post("/", response_model=schemas.DailyTask, status_code=status.HTTP_201_CREATED)
async def create_daily_task(daily_task: schemas.DailyTask,
                            user: schemas.User = Depends(
                                depends.get_current_user),
                            session: Session = Depends(depends.get_session)) -> schemas.DailyTask:

    # create an instance of the dailytask database model
    daily_task_db = models.DailyTask(
        taskName=daily_task.taskName, taskDes=daily_task.taskDes, user=user)

    # add it to the session and commit it
    session.add(daily_task_db)
    session.commit()
    session.refresh(daily_task_db)

    # return the daily task object

    return SchemaUtils.convert_daily_task(daily_task_db)


@router.get("/{id}", response_model=schemas.DailyTask)
def read_daily_task(id: int,
                    user: schemas.User = Depends(depends.get_current_user),
                    session: Session = Depends(depends.get_session)) -> models.DailyTask:

    # get the daily task item with the given id
    # daily_task = session.query(models.DailyTask).get(id)
    daily_task = CRUD.get(session, models.DailyTask, id)

    # check if daily task item with given id exists. If not, raise exception and return 404 not found response
    if not daily_task:
        raise HTTPException(
            status_code=404, detail=f"daily task item with id {id} not found")

    return daily_task


@router.put("/{id}", response_model=schemas.DailyTask)
def update_daily_task(id: int, daily_task: schemas.DailyTask,
                      user: schemas.User = Depends(depends.get_current_user),
                      session: Session = Depends(depends.get_session)) -> models.DailyTask:

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


@router.post("/{id}/complete", response_model=schemas.DailyTask)
def complete_daily_task(id: int,
                        user: models.User = Depends(depends.get_current_user),
                        session: Session = Depends(depends.get_session)) -> schemas.DailyTask:

    # get the daily task item with the given id
    daily_task_db = session.query(models.DailyTask).get(id)

    # check if daily task item with given id exists. If not, raise exception and return 404 not found response
    if not daily_task_db:
        raise HTTPException(
            status_code=404, detail=f"daily task item with id {id} not found")

    record = models.CompletionRecord(
        task=daily_task_db)

    # add it to the session and commit it
    session.add(record)

    # add items to user
    task_items: List[models.TaskItem] = daily_task_db.task_items
    if task_items:
        for item in task_items:
            # check if owns any
            existing_user_item = CRUD.get_with_filter(
                session, models.UserItem, models.UserItem.user_id == user.id, models.UserItem.item_id == item.id)

            if existing_user_item:
                existing_user_item.quantity += item.quantity
            else:
                user_item = models.UserItem(
                    user_id=user.id, item_id=item.id, quantity=item.quantity)
                session.add(user_item)

    session.commit()
    session.refresh(record)

    return SchemaUtils.convert_daily_task(daily_task_db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_task(id: int,
                      user: schemas.User = Depends(depends.get_current_user),
                      session: Session = Depends(depends.get_session)) -> None:

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


@router.get("/", response_model=List[schemas.DailyTask])
def read_daily_task_list(
        user: models.User = Depends(depends.get_current_user),
        session: Session = Depends(depends.get_session)) -> List[schemas.DailyTask]:
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # get all daily task items
    # daily_task_list = session.query(models.DailyTask).filter(
    #     models.DailyTask.user_id == user.uid).all()
    daily_task_list = CRUD.get_multi(
        session,
        models.DailyTask,
        filter_condition=models.DailyTask.user_id == user.id
    )

    return [SchemaUtils.convert_daily_task(t) for t in daily_task_list]
