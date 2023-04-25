FROM python:3.8-slim-buster

WORKDIR /app/

RUN apt-get update \
 && mkdir -p /usr/share/man/man1/ \
 && apt-get install -y \
        default-jre \
        glib-networking-common \
        psmisc \
        software-properties-common \
        unzip \
        wget \
        xvfb \
        gcc \
        make \
        libbz2-dev \
	zlib1g-dev \
	tini \
 && mkdir -p /opt/samtools \
 && cd /opt/samtools \
 && wget https://github.com/samtools/samtools/releases/download/1.15/samtools-1.15.tar.bz2 \
 && tar -xjf samtools-1.15.tar.bz2 \
 && cd samtools-1.15 \
 && ./configure --without-curses --disable-lzma \
 && make \
 && mkdir -p /opt/igv \
 && cd /opt/igv \
 && wget http://data.broadinstitute.org/igv/projects/downloads/2.12/IGV_2.12.3.zip \
 && unzip IGV_2.12.3.zip \
 && pip install poetry \
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
COPY ./app/igv.sh /opt/igv/IGV_2.12.3/igv.sh

ENV C_FORCE_ROOT=1 \
    PYTHONPATH=/app

RUN chmod +x /app/worker-start.sh \
 && mv /app/worker-start.sh /usr/bin/worker-start.sh

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/bin/worker-start.sh"]
