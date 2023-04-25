import time
from typing import Optional, Generator, Dict, Any
from contextlib import contextmanager

from app.core.parse_divaseq import (
    parse_divaseq_run,
    parse_divaseq_template,
)
from app.core.celery_app import celery_app
from app.utils import send_email

from app import models
from app.db.session import SessionLocal


@contextmanager
def session_scope() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@celery_app.task(acks_late=False)
def test_celery(word: str) -> str:
    time.sleep(5)
    return f"test task return {word}"


@celery_app.task(acks_late=False)
def celery_add_run_to_database(run_path: str) -> Optional[str]:
    new_run_name: Optional[str] = None
    with session_scope() as db:
        new_run: Optional[models.Run] = parse_divaseq_run(
            db=db, run_path=run_path
        )
        new_run_name = new_run.name if new_run else None
    return new_run_name


@celery_app.task(acks_late=False)
def celery_add_template_to_database(
    run_id: int, template_path: str, stats_path: str
) -> Optional[str]:
    new_template_name: Optional[str] = None
    with session_scope() as db:
        new_template: Optional[models.Template] = parse_divaseq_template(
            db=db,
            run_id=run_id,
            template_path=template_path,
            stats_path=stats_path,
        )
        new_template_name = new_template.name if new_template else None
    return new_template_name


@celery_app.task(acks_late=False)
def celery_send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> str:
    send_email(
        email_to=email_to,
        subject_template=subject_template,
        html_template=html_template,
        environment=environment,
    )
    return f"email sent to {email_to} with subject: {subject_template}"
