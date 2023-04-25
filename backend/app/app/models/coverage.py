from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .sample import Sample  # noqa: F401


class Coverage(Base):
    id = Column(Integer, primary_key=True, index=True)
    labels = Column(ARRAY(Integer))
    values = Column(ARRAY(Integer))
    sample_id = Column(
        Integer,
        ForeignKey("sample.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    sample = relationship(
        "Sample", uselist=False, back_populates="coverage"
    )
