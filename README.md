# SSGUI

SSGUI is a web application designed to streamline next-generation sequencing data analysis.

## Backend local development

Start the stack with Docker Compose:

```bash
docker compose up -d
```

Then start the live-reloading backend with
```bash
docker compose exec backend /start-reload.sh
```

Now you can open your browser and interact with these URLs:

- Frontend, built with Docker, with routes handled based on the path:
  http://ssgui.lvh.me/
- Backend, JSON based web API based on OpenAPI: http://ssgui.lvh.me/api/
- Automatic interactive documentation with Swagger UI (from the OpenAPI
  backend): http://ssgui.lvh.me/docs/
- Alternative automatic documentation with ReDoc (from the OpenAPI
  backend): http://ssgui.lvh.me/redoc/
- PGAdmin, PostgreSQL web administration: http://pgadmin.lvh.me/
- Traefik UI, to see how the routes are being handled by the proxy:
  http://traefik.lvh.me/

**Note**: The first time you start your stack, it might take a minute for it to
be ready, while the backend waits for the database to be ready and configures
everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker compose logs backend
```

### Test running stack

If your stack is already up and you just want to run the tests, you can use:

```bash
docker compose exec backend /app/tests-start.sh
```

That `/app/tests-start.sh` script just calls `pytest` after making sure that
the rest of the stack is running. If you need to pass extra arguments to
`pytest`, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

```bash
docker compose exec backend bash /app/tests-start.sh -x
```

### Test Coverage

Because the test scripts forward arguments to `pytest`, you can enable test
coverage HTML report generation by passing `--cov-report=html`.

To run the tests in a running stack with coverage HTML reports:

```bash
docker compose exec backend bash /app/tests-start.sh --cov-report=html
```

### Migrations

As during local development your app directory is mounted as a volume inside
the container, you can also run the migrations with `alembic` commands inside
the container and the migration code will be in your app directory (instead of
being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your
database with that revision every time you change them. This is what will
update the tables in your database. If you do not update your database, your
application will have errors as the code will no longer reference the correct
database structure.

Start an interactive session in the backend container:

```console
$ docker compose exec backend bash
```

If you created a new model in `./backend/app/app/models/`, make sure to import
it in `./backend/app/app/db/base.py`, that Python module (`base.py`) that
imports all the models will be used by Alembic.

After changing a model (for example, adding a column), inside the container,
create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

Commit to the git repository the files generated in the alembic directory.

After creating the revision, run the migration in the database (this is what
will actually change the database):

```console
$ alembic upgrade head
```

If you don't want to start with the default models and want to remove them /
modify them, from the beginning, without having any previous revision, you can
remove the revision files (`.py` Python files) under
`./backend/app/alembic/versions/`. And then create a first migration as
described above.

## Frontend development

Enter the `frontend` directory, install the NPM packages and start the live
server using the `npm` scripts:

```bash
cd frontend
npm install
npm run serve
```

Then open your browser at http://localhost:8080/

Notice that this live server is not running inside Docker, it is for local
development, and that is the recommended workflow. Once you are happy with
your frontend, you can build the frontend Docker image and start it, to test
it in a production-like environment. But compiling the image at every change
will not be as productive as running the local development server with
live reload.

Check the file `package.json` to see other available options.

If you have Vue CLI installed, you can also run `vue ui` to control, configure,
serve, and analyze your application using a nice local web user interface.

If you are only developing the frontend (e.g. other team members are developing
the backend) and there is a staging environment already deployed, you can make
your local development code use that staging API instead of a full local
Docker Compose stack.

To do that, modify the file `./frontend/.env`, there's a section with:

```
VUE_APP_ENV=development
# VUE_APP_ENV=staging
```

Switch the comment, to:

```
# VUE_APP_ENV=development
VUE_APP_ENV=staging
```

## Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that
apply to the whole stack, it is used automatically by `docker compose`.

And there's also a `docker-compose.override.yml` with overrides for
development, for example to mount the source code as a volume. It is used
automatically by `docker compose` to apply overrides on top of
`docker-compose.yml`.

These Docker Compose files use the `.env` file containing configurations to be
injected as environment variables in the containers.

They also use some additional configurations taken from environment variables
set in the scripts before calling the `docker compose` command.

## Production deployment

As the application is written as docker microservices, a docker swarm
production deployment is very convenient. Information about deploying
a docker swarm application can be found [here](https://dockerswarm.rocks/).

## Acknowledgements

SSGUI depends on the following separate libraries and packages:

* IGV.js
* PostgreSQL
* RabbitMQ
* Celery
* Traefik
* Pgadmin
* VueJS
* Samtools
* Alembic
* Gunicorn
* FastAPI
* Pydantic
* SQLAlchemy
* Pandas

We thank all their contributors and maintainers!

## Licence

SSGUI is distributed under a modified BSD license. See [LICENSE.txt](LICENSE.txt) for the full license.

## Copyright Notice

View the copyright notice for SSGUI in [LEGAL.txt](LEGAL.txt).
