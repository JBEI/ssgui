from typing import Optional

from pydantic import BaseModel


# Shared properties
class ConsensusBase(BaseModel):
    contents: Optional[str] = None


# Properties to receive on item creation
class ConsensusCreate(ConsensusBase):
    contents: str


# Properties to receive on item update
class ConsensusUpdate(ConsensusBase):
    pass


# Properties shared by models stored in DB
class ConsensusInDBBase(ConsensusCreate):
    id: int
    sample_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Consensus(ConsensusInDBBase):
    pass


# Properties properties stored in DB
class ConsensusInDB(ConsensusInDBBase):
    pass
