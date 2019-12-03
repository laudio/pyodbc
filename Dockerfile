# STAGE: base
# -----------
# The main image that is published.
FROM python:3.7-slim AS base

COPY requirements.txt .

# Setup dependencies for pyodbc
RUN \
  export ACCEPT_EULA='Y' && \
  export FILE_NAME='mysql-connector-odbc-8.0.18-linux-glibc2.12-x86-64bit' && \
  apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https && \
  #
  # Install pyodbc db drivers for MSSQL, PG and MySQL
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  curl -L -o ${FILE_NAME}.tar.gz https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/${FILE_NAME}.tar.gz && \
  apt-get update && \
  gunzip ${FILE_NAME}.tar.gz && \
  tar xvf ${FILE_NAME}.tar && \
  cp ${FILE_NAME}/bin/* /usr/local/bin && \
  cp ${FILE_NAME}/lib/* /usr/local/lib && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so" && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so" && \
  apt-get install -y msodbcsql17 odbc-postgresql && \
  #
  # Update odbcinst.ini to make sure full path to driver is listed
  sed 's/Driver=psql/Driver=\/usr\/lib\/x86_64-linux-gnu\/odbc\/psql/' /etc/odbcinst.ini > /tmp/temp.ini && \
  mv -f /tmp/temp.ini /etc/odbcinst.ini && \
  # Install dependencies
  pip install --upgrade pip && \
  pip install -r requirements.txt && rm requirements.txt && \
  # Cleanup build dependencies
  rm -rf ${FILE_NAME}* && \
  apt-get remove -y curl apt-transport-https debconf-utils g++ gcc rsync unixodbc-dev build-essential gnupg2 && \
  apt-get autoremove -y && apt-get autoclean -y

# STAGE: test
# -----------
# Image used for running tests.
FROM base AS test

WORKDIR /test
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY test ./test

CMD ["pytest", "-v"]
