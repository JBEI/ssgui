import json
from typing import Any, List

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
import celery.bin.amqp

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Test Celery worker"""
    celery_app.send_task(
        "app.worker.test_celery", kwargs={"word": msg.msg}
    )
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Test emails."""
    celery_app.send_task(
        "app.worker.celery_send_email",
        kwargs={
            "email_to": email_to,
            "subject_template": "SSGUI Test Email",
            "html_template": "Test Email. Please Ignore.",
        },
    )
    return {"msg": "Test email queued"}


@router.get(
    "/active-celery-tasks", response_model=List[schemas.CeleryTask]
)
def active_celery_tasks(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """List all active celery tasks

    You can get a list of currently executing tasks
    """
    all_tasks = celery_app.control.inspect().active()
    return [
        schemas.CeleryTask(
            id=task["id"],
            name=task["name"],
            hostname=task["hostname"],
            time_start=task["time_start"],
            acknowledged=task["acknowledged"],
            worker_pid=task["worker_pid"],
            details=json.dumps(task["kwargs"]),
        )
        for worker in all_tasks
        for task in all_tasks[worker]
    ]


@router.get(
    "/reserved-celery-tasks", response_model=List[schemas.CeleryTask]
)
def reserved_celery_tasks(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """List all reserved celery tasks

    Reserved tasks are tasks that have been received, but are still waiting
    to be executed.
    """
    all_tasks = celery_app.control.inspect().reserved()
    return [
        schemas.CeleryTask(
            id=task["id"],
            name=task["name"],
            hostname=task["hostname"],
            time_start=task["time_start"],
            acknowledged=task["acknowledged"],
            worker_pid=task["worker_pid"],
            details=json.dumps(task["kwargs"]),
        )
        for worker in all_tasks
        for task in all_tasks[worker]
    ]


@router.get(
    "/ping-celery-workers", response_model=List[schemas.CeleryWorker]
)
def ping_celery_workers(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Ping all alive workers"""
    ping_response = celery_app.control.ping()
    return [
        schemas.CeleryWorker(name=list(worker.keys())[0])
        for worker in ping_response
    ]


@router.post("/restart-celery-workers")
def restart_celery_workers(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Restart celery workers

    Workers will automatically get restarted by broker after "shutdown"
    signal
    """
    return celery_app.control.broadcast("shutdown")


@router.post("/purge-celery-queue", response_model=schemas.Msg)
def purge_celery_queue(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Purge, discard, and revoke celery queue

    This will stop all active tasks as well tasks waiting in queue
    """
    amqp = celery.bin.amqp.amqp(app=celery_app)
    # Clear queue twice
    for i in [1, 2]:
        amqp.run("queue.purge", "main-queue")
        celery_app.control.purge()
        celery_app.control.discard_all()

        task_ids = []
        active_celery_tasks = celery_app.control.inspect().active()
        reserved_celery_tasks = celery_app.control.inspect().reserved()
        for worker in reserved_celery_tasks:
            for task in reserved_celery_tasks[worker]:
                task_ids.append(task["id"])
        for worker in active_celery_tasks:
            for task in active_celery_tasks[worker]:
                task_ids.append(task["id"])
        celery_app.control.revoke(task_ids, terminate=True)
    return {"msg": "celery queue purged"}


@router.post("/revoke-celery-task/{task_id}")
def revoke_task(
    task_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Revoke particular task by task id

    This will stop an active task
    """
    return celery_app.control.revoke(task_id, terminate=True)


@router.get("/stat-celery-workers")
def stat_celery_workers(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Stats of all celery workers"""
    return celery_app.control.inspect().stats()
