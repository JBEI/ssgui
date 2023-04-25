from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app import crud, schemas
from app.tests import utils


def test_create_run(db: Session) -> None:
    name = utils.random_lower_string()
    run_in = schemas.RunCreate(name=name)
    run = crud.run.create(db=db, obj_in=run_in)
    assert run.name == name


def test_get_run(db: Session) -> None:
    run = utils.create_random_run(db=db)
    stored_run = crud.run.get(db=db, id=run.id)
    assert stored_run
    assert jsonable_encoder(run) == jsonable_encoder(stored_run)


def test_update_run(db: Session) -> None:
    run = utils.create_random_run(db=db)
    name2 = utils.random_lower_string()
    run_update = schemas.RunUpdate(name=name2)
    run2 = crud.run.update(db=db, db_obj=run, obj_in=run_update)
    assert run.id == run2.id
    assert run2.name == name2


def test_delete_run(db: Session) -> None:
    run = utils.create_random_run(db=db)
    run2 = crud.run.remove(db=db, id=run.id)
    run3 = crud.run.get(db=db, id=run.id)
    assert run3 is None
    assert run2.id == run.id
