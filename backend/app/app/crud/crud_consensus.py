from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.consensus import Consensus
from app.schemas.consensus import ConsensusCreate, ConsensusUpdate


class CRUDConsensus(CRUDBase[Consensus, ConsensusCreate, ConsensusUpdate]):
    """CRUD Methods for Consensus"""

    def create(  # type: ignore
        self, db: Session, *, obj_in: ConsensusCreate, sample_id: int
    ) -> Consensus:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, sample_id=sample_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


consensus = CRUDConsensus(Consensus)
