from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.tests import utils

from typing import Optional


def create_random_sample(
    db: Session,
    template_id: Optional[int] = None,
    user_id: Optional[int] = None,
) -> models.Sample:
    if template_id is None:
        template = utils.create_random_template(db=db)
        template_id = template.id
    if user_id is None:
        user = utils.create_random_user(db=db)
        user_id = user.id
    name: str = utils.random_lower_string()
    sample_path: str = utils.random_sample_path()
    obj_in = schemas.SampleCreate(
        name=name,
        gff=utils.random_gff_path(random_sample_path=sample_path),
        genome=utils.random_genome_path(random_sample_path=sample_path),
        length=utils.random_int(),
    )
    return crud.sample.create(
        db=db, obj_in=obj_in, template_id=template_id, user_id=user_id
    )
