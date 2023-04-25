from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .sample import Sample  # noqa: F401


class Consensus(Base):
    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String)
    sample_id = Column(
        Integer,
        ForeignKey("sample.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    sample = relationship(
        "Sample", uselist=False, back_populates="consensus"
    )
