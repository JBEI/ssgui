from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app import crud, schemas
from app.tests import utils


def test_create_template(db: Session) -> None:
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
    template = crud.template.create(db=db, obj_in=obj_in, run_id=run_id)
    assert template.name == name


def test_get_template(db: Session) -> None:
    template = utils.create_random_template(db=db)
    stored_template = crud.template.get(db=db, id=template.id)
    assert stored_template
    assert jsonable_encoder(template) == jsonable_encoder(stored_template)


def test_update_template(db: Session) -> None:
    template = utils.create_random_template(db=db)
    name2 = utils.random_lower_string()
    template_update = schemas.TemplateUpdate(name=name2)
    template2 = crud.template.update(
        db=db, db_obj=template, obj_in=template_update
    )
    assert template.id == template2.id
    assert template2.name == name2


def test_delete_template(db: Session) -> None:
    template = utils.create_random_template(db=db)
    template2 = crud.template.remove(db=db, id=template.id)
    template3 = crud.template.get(db=db, id=template.id)
    assert template3 is None
    assert template2.id == template.id
