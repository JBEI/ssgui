from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests import utils

import os


def test_create_template_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    template_path: str = utils.random_template_path()
    data = {
        "name": os.path.basename(template_path),
        "gff": utils.random_gff_path(random_template_path=template_path),
        "genome": utils.random_genome_path(
            random_template_path=template_path
        ),
        "length": utils.random_int(),
    }
    params = {"run_id": utils.create_random_run(db=db).id}
    response = client.post(
        f"{settings.API_V1_STR}/templates",
        headers=superuser_token_headers,
        json=data,
        params=params,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_template_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    template = utils.create_random_template(db)
    response = client.get(
        f"{settings.API_V1_STR}/templates/{template.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == template.name
    assert content["id"] == template.id


def test_update_template_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    template = utils.create_random_template(db)
    data = {"name": utils.random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/templates/{template.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["id"] == template.id


def test_delete_template_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    template = utils.create_random_template(db)
    response = client.delete(
        f"{settings.API_V1_STR}/templates/{template.id}",
        headers=superuser_token_headers,
    )
    deleted_template = crud.template.get(db=db, id=template.id)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == template.id
    assert deleted_template is None
