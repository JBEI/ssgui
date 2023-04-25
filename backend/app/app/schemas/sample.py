from typing import Optional, List

from app.schemas.template import Template

from pydantic import BaseModel


class Variant(BaseModel):
    position: int
    reference: str
    variant: str
    quality: float
    info: str


# Shared properties
class SampleBase(BaseModel):
    name: Optional[str] = None
    bam: Optional[str] = None
    vcf: Optional[str] = None
    snapshot: Optional[str] = None
    n_reads: Optional[int] = None
    n_r1_reads_aligned: Optional[int] = None
    n_r2_reads_aligned: Optional[int] = None
    average_coverage: Optional[float] = None
    percent_complete: Optional[float] = None
    median_insert_length: Optional[int] = None
    snps: Optional[int] = None
    insertions: Optional[int] = None
    deletions: Optional[int] = None


# Properties to receive on item creation
class SampleCreate(SampleBase):
    name: str
    bam: str
    vcf: str
    snapshot: str
    n_reads: int
    n_r1_reads_aligned: int
    n_r2_reads_aligned: int
    average_coverage: float
    percent_complete: float
    median_insert_length: int
    snps: int
    insertions: int
    deletions: int


# Properties to receive on item update
class SampleUpdate(SampleBase):
    pass


# Properties shared by models stored in DB
class SampleInDBBase(SampleCreate):
    id: int
    template_id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Sample(SampleInDBBase):
    pass


# Properties properties stored in DB
class SampleInDB(SampleInDBBase):
    pass


class IGVTrack(BaseModel):
    type: str
    format: str
    name: str
    url: str
    indexURL: Optional[str] = None


class IGVView(BaseModel):
    fasta_url: str
    index_url: str
    tracks: List[IGVTrack]


class SamplePlusIGV(BaseModel):
    sample: Sample
    template: Template
    igv_view: IGVView
