from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .template import Template  # noqa: F401


class Run(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # Children
    templates = relationship(
        "Template",
        back_populates="run",
        passive_deletes=True,
        cascade="all,delete-orphan",
    )
