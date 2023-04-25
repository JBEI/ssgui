from typing import Optional, Dict

from pydantic import BaseModel, root_validator


# Shared properties
class RunBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on item creation
class RunCreate(RunBase):
    name: str


# Properties to receive on item update
class RunUpdate(RunBase):
    pass


# Properties shared by models stored in DB
class RunInDBBase(RunCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Run(RunInDBBase):
    pass


# Properties properties stored in DB
class RunInDB(RunInDBBase):
    pass


class RunCounts(Run):
    samples_on_disk: int
    samples_in_db: int
    samples_on_disk_match_db: Optional[bool]

    class Config:
        validate_assignment = True

    @root_validator
    def compare_samples_on_disk_vs_db(cls, values: Dict) -> Dict:
        values["samples_on_disk_match_db"] = values.get(
            "samples_on_disk"
        ) == values.get("samples_in_db")
        return values


class RawDivaRun(BaseModel):
    name: str
