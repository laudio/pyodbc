# STAGE: base
# -----------
# The main image that is published.
FROM python:3.6-slim AS base

WORKDIR /source

# Build Constants
ENV ACCEPT_EULA Y

# Setup dependencies for pyodbc
ONBUILD RUN \
  apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https && \
  #
  # Install pyodbc db drivers for MSSQL and PG
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  apt-get update && \
  apt-get install -y msodbcsql17 odbc-postgresql && \
  #
  # Update odbcinst.ini to make sure full path to driver is listed
  sed 's/Driver=psql/Driver=\/usr\/lib\/x86_64-linux-gnu\/odbc\/psql/' /etc/odbcinst.ini > /tmp/temp.ini && \
  mv -f /tmp/temp.ini /etc/odbcinst.ini && \
  # Install pyodbc
  pip install pyodbc==4.0.27 && \
  # Cleanup build dependencies
  apt-get remove -y curl apt-transport-https debconf-utils g++ gcc rsync build-essential gnupg2 && \
  apt-mark manual libssl1.0.2 && apt-get autoremove -y && apt-get autoclean -y

CMD ["python"]

# STAGE: test
# -----------
# Image used for running tests.
FROM base AS test

ONBUILD RUN pip install pytest==4.*
ONBUILD COPY test ./test

CMD ["pytest", "-v"]
