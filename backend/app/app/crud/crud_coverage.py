from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.coverage import Coverage
from app.schemas.coverage import CoverageCreate, CoverageUpdate


class CRUDCoverage(CRUDBase[Coverage, CoverageCreate, CoverageUpdate]):
    """CRUD Methods for Coverages"""

    def create(  # type: ignore
        self, db: Session, *, obj_in: CoverageCreate, sample_id: int
    ) -> Coverage:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, sample_id=sample_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


coverage = CRUDCoverage(Coverage)
