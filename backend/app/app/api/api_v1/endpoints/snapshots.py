from typing import List, Tuple, Optional
import io
import base64
import zipfile

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps


router = APIRouter()


@router.get("/snapshots/{run_id}")
def read_snapshots_by_run(
    run_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> StreamingResponse:
    """Retrieve snapshots by run."""
    samples_and_templates: List[Tuple[models.Sample, models.Template]]
    run: Optional[models.Run] = crud.run.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    if crud.user.is_superuser(current_user):
        samples_and_templates = crud.sample.get_all_by_run_with_templates(
            db=db, run_id=run_id
        )
    else:
        samples_and_templates = (
            crud.sample.get_all_by_user_and_run_with_templates(
                db=db, user_id=current_user.id, run_id=run_id
            )
        )
    snapshot_name: str
    zip_results: io.BytesIO = io.BytesIO()
    with zipfile.ZipFile(zip_results, "w") as archive:
        for sample, template in samples_and_templates:
            snapshot_name = f"{template.name}_{sample.name}.png"
            consensus_name = f"{template.name}_{sample.name}.consensus.fa"
            archive.writestr(
                f"snapshots/{snapshot_name}",
                base64.b64decode(
                    sample.snapshot if sample.snapshot else ""
                ),
            )
            if sample.consensus and sample.consensus.contents:
                archive.writestr(
                    f"consensus/{consensus_name}",
                    sample.consensus.contents,
                )
    zip_results.seek(0)
    return StreamingResponse(zip_results, media_type="application/zip")
