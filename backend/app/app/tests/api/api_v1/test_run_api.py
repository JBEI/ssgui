from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests import utils


def test_create_run_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": utils.random_lower_string()}
    response = client.post(
        f"{settings.API_V1_STR}/runs",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_run_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    run = utils.create_random_run(db)
    response = client.get(
        f"{settings.API_V1_STR}/runs/{run.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == run.name
    assert content["id"] == run.id


def test_update_run_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    run = utils.create_random_run(db)
    data = {"name": utils.random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/runs/{run.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["id"] == run.id


def test_delete_run_with_api(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    run = utils.create_random_run(db)
    response = client.delete(
        f"{settings.API_V1_STR}/runs/{run.id}",
        headers=superuser_token_headers,
    )
    deleted_run = crud.run.get(db=db, id=run.id)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == run.id
    assert deleted_run is None
