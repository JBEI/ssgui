from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate

from typing import List

from app import models


class CRUDTemplate(CRUDBase[Template, TemplateCreate, TemplateUpdate]):
    def create(  # type: ignore
        self, db: Session, *, obj_in: TemplateCreate, run_id: int
    ) -> Template:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, run_id=run_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all_by_user(
        self, db: Session, *, user_id: int
    ) -> List[Template]:
        return (
            db.query(models.Template)
            .join(models.Sample)
            .join(models.User)
            .filter(models.User.id == user_id)
            .all()
        )

    def get_all_by_user_and_run(
        self, db: Session, *, user_id: int, run_id: int
    ) -> List[Template]:
        return (
            db.query(models.Template)
            .join(models.Run)
            .join(models.Sample)
            .join(models.User)
            .filter(models.User.id == user_id)
            .filter(models.Run.id == run_id)
            .all()
        )

    def count_samples(self, db: Session, *, template_id: int) -> int:
        return (
            db.query(models.Sample.id)
            .join(models.Template)
            .filter(models.Template.id == template_id)
            .count()
        )


template = CRUDTemplate(Template)
