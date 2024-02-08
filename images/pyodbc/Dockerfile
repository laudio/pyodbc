# STAGE: base
# -----------
# The main image that is published.
FROM python:3.11-slim-bookworm AS base

COPY requirements.txt .

RUN \
  # Install build dependencies
  apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https && \
  # Install pyodbc db drivers for MSSQL, PostgreSQL and MySQL
  curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg && \
  curl -sSL https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
  apt-get update && \
  ACCEPT_EULA='Y' apt-get install -y msodbcsql18 odbc-postgresql && \
  # Install dependencies (pyobdc)
  pip install --upgrade pip && \
  pip install -r requirements.txt && rm requirements.txt && \
  # Cleanup build dependencies
  apt-get remove -y curl apt-transport-https debconf-utils g++ gcc rsync unixodbc-dev build-essential gnupg2 && \
  apt-get autoremove -y && apt-get autoclean -y

# STAGE: dev
# ----------
# Intermediate image used to install dependencies.
FROM base AS dev

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# STAGE: test
# -----------
# Image used for running tests.
FROM dev AS test

WORKDIR /test
COPY test ./test

CMD pylint -v -E **/*.py && pytest -v

# STAGE: lint-examples
# --------------------
# Image used to lint examples.
FROM dev AS lint-examples

COPY examples ./examples
RUN for f in examples/*/requirements.txt; do pip install -r "$f"; done
CMD pylint -v -E examples/**/*.py
