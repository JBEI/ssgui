from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .run import Run  # noqa: F401
    from .sample import Sample  # noqa: F401


class Template(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gff = Column(String)
    genome = Column(String)
    length = Column(Integer)
    # Run
    run_id = Column(
        Integer,
        ForeignKey("run.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    run = relationship("Run", back_populates="templates")
    # Children
    samples = relationship(
        "Sample",
        back_populates="template",
        passive_deletes=True,
        cascade="all,delete-orphan",
    )
