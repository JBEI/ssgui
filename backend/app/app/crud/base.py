from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete
        (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return (
            db.query(self.model).filter(self.model.id == id).one_or_none()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get_by(
        self,
        db: Session,
        *,
        obj_in: Dict[str, Any],
    ) -> Optional[ModelType]:
        obj_in_data = self._exclude_unset(jsonable_encoder(obj_in))
        db_objs = db.query(self.model).filter_by(**obj_in_data)
        return db_objs.one_or_none()

    def get_all_by(
        self,
        db: Session,
        *,
        obj_in: Dict[str, Any],
    ) -> List[ModelType]:
        obj_in_data = self._exclude_unset(jsonable_encoder(obj_in))
        db_objs = db.query(self.model).filter_by(**obj_in_data)
        return db_objs.all()

    def create(
        self, db: Session, *, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
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

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_all(self, db: Session) -> List[ModelType]:
        objs = self.get_all(db=db)
        for obj in objs:
            db.delete(obj)
        db.commit()
        return objs

    def _exclude_unset(self, d: dict) -> dict:
        """Remove entries in dict with value None

        From: https://medium.com/better-programming/how-to-remove-
        null-none-values-from-a-dictionary-in-python-1bedf1aab5e4
        """
        clean = {}
        for key, value in d.items():
            if isinstance(value, dict):
                nested = self._exclude_unset(value)
                if len(nested.keys()) > 0:
                    clean[key] = nested
            elif value is not None:
                clean[key] = value
        return clean
