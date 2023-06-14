# STAGE: base
# -----------
# The main image that is published.
FROM python:3.11-slim AS base

COPY requirements.txt .

# Setup dependencies for pyodbc
RUN \
  export ACCEPT_EULA='Y' && \
  export MYSQL_CONNECTOR='mysql-connector-odbc-8.0.33-linux-glibc2.28-x86-64bit' && \
  export MYSQL_CONNECTOR_CHECKSUM='41d03d5df0c631f8071cc697f7714620' && \
  # Install build dependencies
  apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https && \
  # Install pyodbc db drivers for MSSQL, PG and MySQL
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  curl -L -o ${MYSQL_CONNECTOR}.tar.gz https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/${MYSQL_CONNECTOR}.tar.gz && \
  curl -L -o ${MYSQL_CONNECTOR}.tar.gz.asc https://downloads.mysql.com/archives/gpg/\?file\=${MYSQL_CONNECTOR}.tar.gz\&p\=10 && \
  echo "${MYSQL_CONNECTOR_CHECKSUM} ${MYSQL_CONNECTOR}.tar.gz" | md5sum -c - && \
  apt-get update && \
  gunzip ${MYSQL_CONNECTOR}.tar.gz && tar xvf ${MYSQL_CONNECTOR}.tar && \
  cp -r ${MYSQL_CONNECTOR}/bin/* /usr/local/bin && cp -r ${MYSQL_CONNECTOR}/lib/* /usr/local/lib && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so" && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so" && \
  apt-get install -y msodbcsql18 odbc-postgresql && \
  # Update odbcinst.ini to make sure full path to driver is listed, and set CommLog to 0. i.e disables any communication logs to be written to files
  sed 's/Driver=psql/Driver=\/usr\/lib\/x86_64-linux-gnu\/odbc\/psql/;s/CommLog=1/CommLog=0/' /etc/odbcinst.ini > /tmp/temp.ini && \
  mv -f /tmp/temp.ini /etc/odbcinst.ini && \
  # Install dependencies
  pip install --upgrade pip && \
  pip install -r requirements.txt && rm requirements.txt && \
  # Cleanup build dependencies
  rm -rf ${MYSQL_CONNECTOR}* && \
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
