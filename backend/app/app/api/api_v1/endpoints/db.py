from fastapi import APIRouter, Depends, HTTPException

from app import schemas, models
from app.api import deps
from app.core.celery_app import celery_app
from app.core.config import settings

from typing import Any, List
import re
import os
import glob
import logging

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@router.post("/db/update", response_model=schemas.Msg, status_code=201)
async def update_database(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Loads database with info about divaseq data"""
    run_names: List[str] = glob.glob(
        f"{settings.SEQUENCING_DATA_DIR}/[0-9]*_M03257_[0-9]*_[0-9]*"
    )
    for dir in run_names:
        if re.match(".*de_novo.*", dir):
            run_names.remove(dir)
    logger.debug(f"Detected runs: {run_names}")
    for run_path in run_names:
        celery_app.send_task(
            "app.worker.celery_add_run_to_database",
            kwargs={"run_path": run_path},
        )
    return {"msg": "Database will update in background"}


@router.post(
    "/db/update_run/{run_name}",
    response_model=schemas.Msg,
    status_code=201,
)
async def update_database_run(
    run_name: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Loads database with info about divaseq data"""
    run_path: str = f"{settings.SEQUENCING_DATA_DIR}/{run_name}"
    if os.path.exists(run_path):
        celery_app.send_task(
            "app.worker.celery_add_run_to_database",
            kwargs={"run_path": run_path},
        )
    else:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"msg": "Database will update in background"}


@router.get(
    "/db/raw_diva_runs",
    response_model=List[schemas.RawDivaRun],
)
async def get_raw_diva_runs(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> List[schemas.RawDivaRun]:
    """Reads /diva share and lists available diva runs"""
    run_names: List[str] = glob.glob(
        f"{settings.SEQUENCING_DATA_DIR}/[0-9]*_M03257_[0-9]*_[0-9]*"
    )
    for dir in run_names:
        if re.match(".*de_novo.*", dir):
            run_names.remove(dir)
    return [schemas.RawDivaRun(name=name) for name in run_names]
