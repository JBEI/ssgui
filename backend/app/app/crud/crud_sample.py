from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.sample import Sample
from app.schemas.sample import (
    SampleCreate,
    SampleUpdate,
)

from typing import List, Tuple

from app import models


class CRUDSample(CRUDBase[Sample, SampleCreate, SampleUpdate]):
    """CRUD Methods for Samples"""

    def create(  # type: ignore
        self,
        db: Session,
        *,
        obj_in: SampleCreate,
        user_id: int,
        template_id: int
    ) -> Sample:
        obj_in_data = jsonable_encoder(obj_in)

        db_obj = self.model(
            **obj_in_data,
            user_id=user_id,
            template_id=template_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all_by_run(self, db: Session, *, run_id: int) -> List[Sample]:
        return (
            db.query(models.Sample)
            .join(models.Template)
            .join(models.Run)
            .filter(models.Run.id == run_id)
            .all()
        )

    def get_all_by_user_and_run(
        self, db: Session, *, user_id: int, run_id: int
    ) -> List[Sample]:
        return (
            db.query(models.Sample)
            .join(models.Template)
            .join(models.Run)
            .filter(models.Sample.user_id == user_id)
            .filter(models.Run.id == run_id)
            .all()
        )

    def get_all_by_run_with_templates(
        self, db: Session, *, run_id: int
    ) -> List[Tuple[Sample, models.Template]]:
        return (
            db.query(
                models.Sample,
                models.Template,
            )
            .join(models.Template)
            .join(models.Run)
            .filter(models.Run.id == run_id)
            .all()
        )

    def get_all_by_user_and_run_with_templates(
        self, db: Session, *, user_id: int, run_id: int
    ) -> List[Tuple[Sample, models.Template]]:
        return (
            db.query(models.Sample, models.Template)
            .join(models.Template)
            .join(models.Run)
            .filter(models.Sample.user_id == user_id)
            .filter(models.Run.id == run_id)
            .all()
        )


sample = CRUDSample(Sample)
