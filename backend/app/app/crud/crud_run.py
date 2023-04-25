from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.run import Run
from app.schemas.run import RunCreate, RunUpdate

from app import models

from typing import List


class CRUDRun(CRUDBase[Run, RunCreate, RunUpdate]):
    """CRUD Methods for Runs"""

    def get_all_by_user(self, db: Session, *, user_id: int) -> List[Run]:
        return (
            db.query(self.model)
            .join(models.Template)
            .join(models.Sample)
            .join(models.User)
            .filter(models.User.id == user_id)
            .all()
        )

    def count_samples(self, db: Session, *, run_id: int) -> int:
        return (
            db.query(models.Sample.id)
            .join(models.Template)
            .join(models.Run)
            .filter(models.Run.id == run_id)
            .count()
        )


run = CRUDRun(Run)
