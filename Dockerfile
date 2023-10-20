FROM python:3.11.6-slim-bookworm AS development_build

ENV DJANGO_ENV=development \
  # python:
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry" && poetry --version

# set work directory
WORKDIR /code

COPY pyproject.toml poetry.lock /code/

# Install dependencies:
RUN poetry install
COPY . .

RUN poetry run python manage.py migrate

EXPOSE 8000
CMD poetry run python manage.py runserver 0.0.0.0:8000
