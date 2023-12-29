FROM laudio/pyodbc:2.1.0 AS base

USER root

ENV ACCEPT_EULA=Y

RUN apt-get install -y debconf-utils \
  && apt-get update -y \
  && apt-get -y install mssql-tools unixodbc-dev

ENV PATH="$PATH:/opt/mssql-tools/bin"

FROM base AS test

WORKDIR /test

COPY requirements-dev.txt .
RUN pip install --upgrade pip && pip install -r requirements-dev.txt

COPY test ./test

CMD pylint -v -E **/*.py && pytest -vvv
