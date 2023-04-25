from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .template import Template  # noqa: F401
    from .user import User  # noqa: F401
    from .consensus import Consensus  # noqa: F401
    from .coverage import Coverage  # noqa: F401


class Sample(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    bam = Column(String)
    vcf = Column(String)
    snapshot = Column(String)
    n_reads = Column(Integer)
    n_r1_reads_aligned = Column(Integer)
    n_r2_reads_aligned = Column(Integer)
    average_coverage = Column(Float)
    percent_complete = Column(Float)
    median_insert_length = Column(Integer)
    snps = Column(Integer)
    insertions = Column(Integer)
    deletions = Column(Integer)
    consensus = relationship(
        "Consensus",
        back_populates="sample",
        uselist=False,
        passive_deletes=True,
        cascade="all,delete-orphan",
    )
    coverage = relationship(
        "Coverage",
        back_populates="sample",
        uselist=False,
        passive_deletes=True,
        cascade="all,delete-orphan",
    )
    template_id = Column(
        Integer,
        ForeignKey("template.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    template = relationship("Template", back_populates="samples")
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    user = relationship("User", back_populates="samples")
