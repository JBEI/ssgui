import io
import os
import zipfile
from typing import Any, List, Tuple, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.core.igv import prepare_igv_view

router = APIRouter()


def check_sample_permissions(
    db: Session, current_user: models.User, sample_id: int
) -> schemas.Sample:
    """Get sample and check if user has permission to read"""
    potential_sample: Optional[models.Sample] = crud.sample.get(
        db=db, id=sample_id
    )
    if not potential_sample:
        raise HTTPException(status_code=404, detail="sample not found")
    if not potential_sample.user_id:
        raise HTTPException(
            status_code=500, detail="sample has no user_id"
        )
    sample: schemas.Sample = schemas.Sample.from_orm(potential_sample)
    if not crud.user.is_superuser(current_user):
        users_who_can_read_sample: List[int] = [sample.user_id]
        if current_user.id not in users_who_can_read_sample:
            raise HTTPException(
                status_code=400, detail="Not enough permissions"
            )
    return sample


@router.get("/samples", response_model=List[schemas.Sample])
def read_samples(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve samples."""
    if crud.user.is_superuser(current_user):
        samples = crud.sample.get_all(db=db)
    else:
        samples = crud.sample.get_all_by(
            db=db, obj_in={"user_id": current_user.id}
        )
    return samples


@router.get(
    "/samples_by_run/{run_id}", response_model=List[schemas.Sample]
)
def read_samples_by_run(
    run_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve samples by run with extra information."""
    run: Optional[models.Run] = crud.run.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    if crud.user.is_superuser(current_user):
        samples = crud.sample.get_all_by_run(db=db, run_id=run_id)
    else:
        samples = crud.sample.get_all_by_user_and_run(
            db=db, user_id=current_user.id, run_id=run_id
        )
    return samples


@router.get(
    "/samples_by_run_with_igv/{run_id}",
    response_model=List[schemas.SamplePlusIGV],
)
def read_samples_by_run_with_igv(
    run_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve samples by run with extra information."""
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
    samples_plus_igv: List[schemas.SamplePlusIGV] = [
        schemas.SamplePlusIGV(
            sample=sample,
            template=template,
            igv_view=prepare_igv_view(
                sample=schemas.Sample.from_orm(sample),
                template=schemas.Template.from_orm(template),
            ),
        )
        for sample, template in samples_and_templates
    ]
    return samples_plus_igv


@router.post("/samples", response_model=schemas.Sample)
def create_sample(
    *,
    db: Session = Depends(deps.get_db),
    sample_in: schemas.SampleCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    template_id: int,
) -> Any:
    """Create new sample."""
    sample = crud.sample.create(
        db=db,
        obj_in=sample_in,
        user_id=current_user.id,
        template_id=template_id,
    )
    return sample


@router.put("/samples/{id}", response_model=schemas.Sample)
def update_sample(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    sample_in: schemas.SampleUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Update a sample."""
    sample = crud.sample.get(db=db, id=id)
    if not sample:
        raise HTTPException(status_code=404, detail="sample not found")
    sample = crud.sample.update(db=db, db_obj=sample, obj_in=sample_in)
    return sample


@router.get("/samples/{id}", response_model=schemas.Sample)
def read_sample(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get sample by ID."""
    sample: schemas.Sample = check_sample_permissions(
        db=db, current_user=current_user, sample_id=id
    )
    return sample


@router.delete("/samples/{id}", response_model=schemas.Sample)
def delete_sample(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Delete a sample."""
    sample = crud.sample.get(db=db, id=id)
    if not sample:
        raise HTTPException(status_code=404, detail="sample not found")
    sample = crud.sample.remove(db=db, id=id)
    return sample


@router.get("/samples/{id}/rawdata")
def read_sample_rawdata(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> StreamingResponse:
    """Get sample raw data by ID.

    Returns a zip file containing: .bam, .bam.bai, .vcf, .vcf.idx,
    .fa, and .fa.fai
    """
    sample: schemas.Sample = check_sample_permissions(
        db=db, current_user=current_user, sample_id=id
    )
    potential_template: Optional[models.Template] = crud.template.get(
        db=db, id=sample.template_id
    )
    if not potential_template:
        raise HTTPException(status_code=404, detail="template not found")
    template: schemas.Template = schemas.Template.from_orm(
        potential_template
    )
    zip_results: io.BytesIO = io.BytesIO()
    with zipfile.ZipFile(zip_results, "w") as archive:
        with open(sample.bam, "rb") as F:
            archive.writestr(os.path.basename(sample.bam), F.read())
        with open(sample.bam + ".bai", "rb") as F:
            archive.writestr(
                os.path.basename(sample.bam) + ".bai", F.read()
            )
        with open(sample.vcf, "rb") as F:
            archive.writestr(os.path.basename(sample.vcf), F.read())
        with open(sample.vcf + ".idx", "rb") as F:
            archive.writestr(
                os.path.basename(sample.vcf) + ".idx", F.read()
            )
        with open(template.genome, "rb") as F:
            archive.writestr(os.path.basename(template.genome), F.read())
        with open(template.genome + ".fai", "rb") as F:
            archive.writestr(
                os.path.basename(template.genome) + ".fai", F.read()
            )
        with open(template.gff, "rb") as F:
            archive.writestr(os.path.basename(template.gff), F.read())
    zip_results.seek(0)
    return StreamingResponse(zip_results, media_type="application/zip")


import numpy as np


def filter_coverage_for_frontend(
    coverage: schemas.Coverage,
) -> schemas.Coverage:
    filtered_labels: List[int] = coverage.labels
    kernel = np.ones(15) / 15
    data_convolved = np.convolve(
        coverage.values, kernel, mode="same"
    ).astype(int)
    filtered_values: List[int] = data_convolved.tolist()
    return schemas.Coverage(
        id=coverage.id,
        sample_id=coverage.sample_id,
        labels=filtered_labels,
        values=filtered_values,
    )


@router.get("/samples/{id}/coverage", response_model=schemas.Coverage)
def read_sample_coverage(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.Coverage:
    """Get sample coverage"""
    potential_coverage: Optional[models.Coverage] = crud.coverage.get_by(
        db=db, obj_in={"sample_id": id}
    )
    if not potential_coverage:
        raise HTTPException(
            status_code=404, detail="sample coverage not found"
        )
    check_sample_permissions(
        db=db, current_user=current_user, sample_id=id
    )
    filtered_coverage: schemas.Coverage = filter_coverage_for_frontend(
        coverage=schemas.Coverage.from_orm(potential_coverage)
    )
    return filtered_coverage
