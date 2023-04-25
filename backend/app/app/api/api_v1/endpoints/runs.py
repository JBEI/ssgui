from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.core.parse_divaseq import count_run_samples

router = APIRouter()


@router.get("/runs", response_model=List[schemas.Run])
def read_runs(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve runs."""
    if crud.user.is_superuser(current_user):
        runs = crud.run.get_all(db=db)
    else:
        runs = crud.run.get_all_by_user(
            db=db,
            user_id=current_user.id,
        )
    return runs


@router.post("/runs", response_model=schemas.Run)
def create_run(
    *,
    db: Session = Depends(deps.get_db),
    run_in: schemas.RunCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Create new run."""
    run = crud.run.create(
        db=db,
        obj_in=run_in,
    )
    return run


@router.put("/runs/{id}", response_model=schemas.Run)
def update_run(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    run_in: schemas.RunUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Update a run."""
    run = crud.run.get(db=db, id=id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    run = crud.run.update(db=db, db_obj=run, obj_in=run_in)
    return run


@router.get("/runs/{id}", response_model=schemas.Run)
def read_run(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get run by ID."""
    run = crud.run.get(db=db, id=id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    if not crud.user.is_superuser(current_user):
        users_who_can_read_run: List[int] = crud.user.get_run_users(
            db=db, run_id=id
        )
        if current_user.id not in users_who_can_read_run:
            raise HTTPException(
                status_code=400, detail="Not enough permissions"
            )
    return run


@router.delete("/runs/{id}", response_model=schemas.Run)
def delete_run(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Delete a run."""
    run = crud.run.get(db=db, id=id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    run = crud.run.remove(db=db, id=id)
    return run


@router.delete("/runs", response_model=List[schemas.Run])
def delete_runs(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Delete all runs from database, clearing it"""
    deleted_runs = crud.run.remove_all(db=db)
    return deleted_runs


@router.get("/runs/{id}/count", response_model=schemas.RunCounts)
def read_run_sample_count(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Count number of samples for a given run."""
    run = crud.run.get(db=db, id=id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    return count_run_samples(db=db, run=schemas.Run.from_orm(run))
