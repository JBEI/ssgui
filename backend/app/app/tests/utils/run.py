from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.tests import utils


def create_random_run(db: Session) -> models.Run:
    obj_in = schemas.RunCreate(name=utils.random_lower_string())
    return crud.run.create(db=db, obj_in=obj_in)
