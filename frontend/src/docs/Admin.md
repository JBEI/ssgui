# Admin Help

## Dashboard

From the _Dashboard_, you will be able to see all runs that have been loaded into the database. If you click on a run, you will be able to see all samples that have been loaded for that run. A non-superuser account will only see runs for which they have samples and will only be able to see samples belonging to them if they click a run.

## Manage Users

From the _Manage Users_ page, you will be able to see each account that has been created for SSGUI. Each account will list the email address which is used to login, account name, whether the account is active, and whether the account is a superuser. It is also from this page that you will be able to edit a user account. This includes the ability to change an accounts user name, email address, superuser status, active status, and password.

<div class="note">

**Note:**
Since the SSGUI automated password reset service has not yet been set up, password resets must be done by an administrator from the _Manage Users_ page. User passwords are not recoverable and must be reset if forgotten. You may use a secrets service to forward secrets to users.

</div>

## Create User

From the _Create User_ page, you will be able to create a new user.

## Manage Database

From the _Manage Database_ page, you will be able to queue a task in the background to update the database by clicking the `Update Database` button. The following events happen upon clicking that button:

1. A POST request is sent to the backend API with your superuser credentials
2. The backend API validates your superuser credentials and enqueues a `celery_add_run_to_database` task for each run in the `/diva/` shared directory.
3. Each task that is queued gets sent to the RabbitMQ broker which delegates task to a celery worker running in a separate container in the swarm.
4. The celery worker upon recieving a task acknowledges the task which removes it from the queue and processes the corresponding run. This includes taking snapshots of each sample using IGV in a subprocess. After processing the run, the run metadata gets added to the database by the celery worker before returning a completion status.
5. All tasks will be processed by the celery worker until no tasks remain in the queue.

To view tasks in the queue which have not yet been completed, use this endpoint: `/api/v1/utils/reserved-celery-tasks`

To view tasks which are actively being processed, use this endpoint: `/api/v1/utils/active-celery-tasks`

To remove all tasks from the queue, use this endpoint: `/api/v1/utils/purge-celery-queue`

To restart all celery workers, use this endpoint: `/api/v1/utils/restart-celery-workers`
