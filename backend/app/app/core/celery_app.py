from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.celery_add_run_to_database": "main-queue",
    "app.worker.celery_add_template_to_database": "main-queue",
    "app.worker.celery_send_email": "main-queue",
}
