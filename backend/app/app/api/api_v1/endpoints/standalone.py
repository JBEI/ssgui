import io

from app import models
from app.core.predict_success import predict_sample_success

from app.api import deps
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/successpred")
async def standalone_success_pred(
    input1: str,
    input2: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> StreamingResponse:
    """Read data and predict sample success"""
    results_file: io.BytesIO = io.BytesIO()
    predict_sample_success(input1, input2)
    return StreamingResponse(results_file, media_type="application/zip")
