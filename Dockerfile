FROM python:3.11-slim AS builder

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"

# install poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /calories_bot

# copy only pyproject.toml and poetry.lock file nothing else here
COPY poetry.lock pyproject.toml ./

# this will create the folder /calories_bot/.venv (might need adjustment depending on which poetry version you are using)
RUN poetry install --no-root --no-ansi

RUN poetry run pip install setuptools

# ---------------------------------------------------------------------

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/calories_bot/.venv/bin:$PATH"

WORKDIR /calories_bot

COPY ./calories_bot calories_bot

# copy the venv folder from builder image
COPY --from=builder /calories_bot/.venv ./.venv

CMD ["python3", "-m", "calories_bot"]