import pandera as pa
from pandera.typing import Series

from pydantic import BaseModel


class SequencingStats(pa.SchemaModel):
    Sample_Name: Series[str] = pa.Field(unique=True)
    N_Reads: Series[int] = pa.Field(alias="#_Reads_(PF)", ge=0)
    N_R1_Reads_Aligned: Series[int] = pa.Field(
        alias="#_R1_Reads_Aligned", ge=0
    )
    N_R2_Reads_Aligned: Series[int] = pa.Field(
        alias="#_R2_Reads_Aligned", ge=0
    )
    Average_Coverage: Series[float] = pa.Field(ge=0)
    Percent_Complete: Series[float] = pa.Field(alias="%_Complete", ge=0)
    Reference_ID: Series[str] = pa.Field()
    Reference_Length: Series[int] = pa.Field(ge=1)
    Median_Insert_Length: Series[int] = pa.Field(ge=0)
    SNPs: Series[int] = pa.Field(ge=0)
    Insertions: Series[int] = pa.Field(ge=0)
    Deletions: Series[int] = pa.Field(ge=0)

    class Config:
        strict = True
        coerce = True


class TemplateStats(BaseModel):
    length: int


class SampleStats(BaseModel):
    n_reads: int
    n_r1_reads_aligned: int
    n_r2_reads_aligned: int
    average_coverage: float
    percent_complete: float
    median_insert_length: int
    snps: int
    insertions: int
    deletions: int
