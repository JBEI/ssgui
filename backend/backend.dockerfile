FROM tiangolo/uvicorn-gunicorn:python3.8-slim

WORKDIR /app/

RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /usr/share/man/man1/ \
 && find /usr/local -name '*.pyc' -delete \
 && find /usr/local -name '__pycache__' -delete

COPY ./app/pyproject.toml ./app/poetry.lock /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ]; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app /app
ENV PYTHONPATH=/app
