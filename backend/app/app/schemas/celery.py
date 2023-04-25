from pydantic import BaseModel
from typing import Optional


class CeleryWorker(BaseModel):
    name: str


class CeleryTask(BaseModel):
    id: str
    name: str
    hostname: str
    time_start: Optional[float] = None
    acknowledged: bool
    worker_pid: Optional[int] = None
    details: str
