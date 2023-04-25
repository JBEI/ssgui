from typing import Optional, List, Dict, Any

import pandera as pa
from pandera.typing import Series

from pydantic import BaseModel, validator


class SamtoolsCoverage(pa.SchemaModel):
    CHROM: Series[str] = pa.Field()
    LOC: Series[int] = pa.Field(ge=0)
    DEPTH: Series[int] = pa.Field(ge=0)

    class Config:
        strict = True
        coerce = True


# Shared properties
class CoverageBase(BaseModel):
    labels: Optional[List[int]] = None
    values: Optional[List[int]] = None


# Properties to receive on item creation
class CoverageCreate(CoverageBase):
    labels: List[int]
    values: List[int]

    @validator("values")
    def lengths_must_match(
        cls, v: List[int], values: Dict[str, Any]
    ) -> List[int]:
        if len(v) != len(values["labels"]):
            raise ValueError(
                "Length of labels does not match length of values"
            )
        return v


# Properties to receive on item update
class CoverageUpdate(CoverageBase):
    pass


# Properties shared by models stored in DB
class CoverageInDBBase(CoverageCreate):
    id: int
    sample_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Coverage(CoverageInDBBase):
    pass


# Properties properties stored in DB
class CoverageInDB(CoverageInDBBase):
    pass
