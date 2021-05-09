FROM tiangolo/uvicorn-gunicorn:python3.7

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install --no-root --no-dev

# Copy project specific files
COPY ./Makefile ./setup.cfg ./
COPY ./desafio ./desafio

# Setup image environment
ENV MODULE_NAME desafio.entrypoints.fastapi.main
ENV VARIABLE_NAME app
