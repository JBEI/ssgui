from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.core.parse_divaseq import count_template_samples

router = APIRouter()


@router.get("/templates", response_model=List[schemas.Template])
def read_templates(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve templates."""
    if crud.user.is_superuser(current_user):
        templates = crud.template.get_all(db=db)
    else:
        templates = crud.template.get_all_by_user(
            db=db,
            user_id=current_user.id,
        )
    return templates


@router.get(
    "/templates_by_run/{run_id}", response_model=List[schemas.Template]
)
def read_templates_by_run(
    run_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve templates for a given run and user"""
    if crud.user.is_superuser(current_user):
        templates = crud.template.get_all_by(
            db=db, obj_in={"run_id": run_id}
        )
    else:
        templates = crud.template.get_all_by_user_and_run(
            db=db,
            user_id=current_user.id,
            run_id=run_id,
        )
    return templates


@router.post("/templates", response_model=schemas.Template)
def create_template(
    *,
    db: Session = Depends(deps.get_db),
    template_in: schemas.TemplateCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    run_id: int,
) -> Any:
    """Create new template."""
    template = crud.template.create(
        db=db, obj_in=template_in, run_id=run_id
    )
    return template


@router.put("/templates/{id}", response_model=schemas.Template)
def update_template(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    template_in: schemas.TemplateUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Update a template."""
    template = crud.template.get(db=db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="template not found")
    template = crud.template.update(
        db=db, db_obj=template, obj_in=template_in
    )
    return template


@router.get("/templates/{id}", response_model=schemas.Template)
def read_template(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get template by ID."""
    template = crud.template.get(db=db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="template not found")
    if not crud.user.is_superuser(current_user):
        users_who_can_read_template: List[
            int
        ] = crud.user.get_template_users(db=db, template_id=id)
        if current_user.id not in users_who_can_read_template:
            raise HTTPException(
                status_code=400, detail="Not enough permissions"
            )
    return template


@router.delete("/templates/{id}", response_model=schemas.Template)
def delete_template(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Delete a template."""
    template = crud.template.get(db=db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="template not found")
    template = crud.template.remove(db=db, id=id)
    return template


@router.get("/templates/{id}/count", response_model=schemas.TemplateCounts)
def read_template_sample_count(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Count number of samples for a given template."""
    template = crud.template.get(db=db, id=id)
    if not template:
        raise HTTPException(status_code=404, detail="template not found")
    return count_template_samples(
        db=db, template=schemas.Template.from_orm(template)
    )
