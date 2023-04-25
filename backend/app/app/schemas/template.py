from typing import Optional, Dict

from pydantic import BaseModel, root_validator


# Shared properties
class TemplateBase(BaseModel):
    name: Optional[str] = None
    gff: Optional[str] = None
    genome: Optional[str] = None
    length: Optional[int] = None


# Properties to receive on item creation
class TemplateCreate(TemplateBase):
    name: str
    gff: str
    genome: str
    length: int


# Properties to receive on item update
class TemplateUpdate(TemplateBase):
    pass


# Properties shared by models stored in DB
class TemplateInDBBase(TemplateCreate):
    id: int
    run_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Template(TemplateInDBBase):
    pass


# Properties properties stored in DB
class TemplateInDB(TemplateInDBBase):
    pass


class TemplateCounts(Template):
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
