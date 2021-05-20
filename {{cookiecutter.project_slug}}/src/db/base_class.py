from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

import pytz
from dictalchemy import DictableModel
from pydantic import BaseModel
from sqlalchemy import MetaData, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.config import settings
from src.utils import get_db_id

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
_Base = declarative_base(cls=DictableModel, metadata=metadata)


class Base(_Base):
    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: get_db_id())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Integer, default=0)


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update,
        Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self,
                  db: Session,
                  *,
                  skip: int = 0,
                  limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by(self, db: Session, condition: dict) -> List[ModelType]:
        return db.query(self.model).filter_by(**condition).all()

    def get_one(self, db: Session, condition: dict) -> List[ModelType]:
        return db.query(self.model).filter_by(**condition).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in)  # type: ignore
        db_obj.created_at = datetime.now(tz=pytz.timezone(settings.SERVER_TZ))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, *, db_obj: ModelType,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in db_obj.__dict__.keys():
            if field in update_data.keys():
                setattr(db_obj, field, update_data[field])
        db_obj.updated_at = datetime.now(tz=pytz.timezone(settings.SERVER_TZ))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int,
               soft_delete: bool = True) -> ModelType:
        obj = db.query(self.model).filter(self.model.id == id).first()

        if soft_delete:
            obj.is_deleted = 1
            obj.updated_at = datetime.now(tz=pytz.timezone(settings.SERVER_TZ))
            db.add(obj)
            db.commit()
            db.refresh(obj)
        else:
            db.delete(obj)
            db.commit()
        return obj
