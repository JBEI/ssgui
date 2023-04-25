from app.tests.utils.db import TestingSessionLocal

from typing import Generator, Any


def override_get_db() -> Generator[Any, None, None]:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
