from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import ClauseElement
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from database import Base

# We need to use a different type variable for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    @staticmethod
    def get(db: Session, model: Type[ModelType], id: int) -> Optional[ModelType]:
        try:
            return db.query(model).filter(model.id == id).one()
        except NoResultFound:
            return None

    @staticmethod
    def get_multi(
        session: Session,
        model: Type[ModelType],
        *,
        skip: int = 0,
        limit: int = 100,
        filter_condition: Optional[ClauseElement] = None
    ) -> List[ModelType]:
        query = session.query(model)
        if filter_condition is not None:
            query = query.filter(filter_condition)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, model: Type[ModelType], *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(
        db: Session,
        model: Type[ModelType],
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def remove(db: Session, model: Type[ModelType], id: int) -> Optional[ModelType]:
        obj = db.query(model).get(id)
        if obj is not None:
            db.delete(obj)
            db.commit()
        return obj


'''

from pydantic import BaseModel
from sqlalchemy.orm import Session

# 定义模型
class YourModel(BaseModel):
    id: int
    # 其他属性

# 创建数据库会话对象
db = Session()

# 调用静态方法
obj = CRUD.get(db, YourModel, id=1)
objs = CRUD.get_multi(db, YourModel, skip=0, limit=10)

# 创建对象
create_data = {"id": 1, ...}  # 创建模型的输入数据
created_obj = CRUD.create(db, YourModel, obj_in=create_data)

# 更新对象
update_data = {"name": "New Name"}  # 更新模型的输入数据
updated_obj = CRUD.update(db, YourModel, db_obj=created_obj, obj_in=update_data)

# 删除对象
deleted_obj = CRUD.remove(db, YourModel, id=1)

'''
