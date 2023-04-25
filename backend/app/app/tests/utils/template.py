from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.tests import utils

from typing import Optional


def create_random_template(
    db: Session, run_id: Optional[int] = None
) -> models.Template:
    if run_id is None:
        run = utils.create_random_run(db=db)
        run_id = run.id
    name: str = utils.random_lower_string()
    template_path: str = utils.random_template_path()
    obj_in = schemas.TemplateCreate(
        name=name,
        gff=utils.random_gff_path(random_template_path=template_path),
        genome=utils.random_genome_path(
            random_template_path=template_path
        ),
        length=utils.random_int(),
    )
    return crud.template.create(db=db, obj_in=obj_in, run_id=run_id)
