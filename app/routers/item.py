from fastapi import APIRouter, Cookie, Request, HTTPException
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from crud import CRUD
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import depends

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()


@router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: schemas.Item,
                      user: schemas.User = Depends(
                          depends.get_current_user),
                      session: Session = Depends(depends.get_session)) -> models.Item:

    item_db = models.Item(
        name=item.name, icon=item.icon, user=user)

    session.add(item_db)
    session.commit()
    session.refresh(item_db)

    return item_db


@router.get("/{id}", response_model=schemas.Item)
def read_item(id: int,
              user: schemas.User = Depends(depends.get_current_user),
              session: Session = Depends(depends.get_session)) -> models.Item:

    item = CRUD.get(session, models.Item, id)

    if not item:
        raise HTTPException(
            status_code=404, detail=f"item with id {id} not found")

    return item


@router.put("/{id}", response_model=schemas.Item)
def update_item(id: int, item: schemas.Item,
                user: schemas.User = Depends(depends.get_current_user),
                session: Session = Depends(depends.get_session)) -> models.Item:

    item_db = session.query(models.Item).get(id)

    if item_db:
        item.name = item.name
        item.icon = item.icon
        session.commit()

    if not item_db:
        raise HTTPException(
            status_code=404, detail=f"daily task item with id {id} not found")

    return item_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int,
                user: schemas.User = Depends(depends.get_current_user),
                session: Session = Depends(depends.get_session)) -> None:

    item = session.query(models.Item).get(id)

    if item:
        session.delete(item)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"dailytask item with id {id} not found")

    return None


@router.get("/", response_model=List[schemas.Item])
def read_item_list(
        user: models.User = Depends(depends.get_current_user),
        session: Session = Depends(depends.get_session)) -> List[models.Item]:
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    item_list = CRUD.get_multi(
        session,
        models.Item,
        filter_condition=models.Item.user_id == user.id
    )

    return item_list
