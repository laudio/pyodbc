[![Build](https://github.com/laudio/pyodbc/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/laudio/pyodbc/actions/workflows/ci.yml)
[![LICENSE](https://img.shields.io/github/license/laudio/pyodbc.svg?style=flat-square)](https://github.com/laudio/pyodbc/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/laudio/pyodbc)

# pyodbc

Docker image with python 3.11 and [pyodbc](https://github.com/mkleehammer/pyodbc). Includes ODBC drivers for MSSQL, PostgreSQL and MySQL.

## Usage

### Pull the image

```bash
$ docker pull laudio/pyodbc
```

### Usage as a base image

Use `laudio/pyodbc` as a base image for your python script.

```Dockerfile
FROM laudio/pyodbc:3.0.0

WORKDIR /app

# Add your source files.
COPY ["src", "./src"]
COPY ["setup.py", "./"]

RUN pip install .

CMD ["python", "src/main.py"]
```

## Development (Contributing)

```bash
# 1. Clone this repository.
$ git clone git@github.com:laudio/pyodbc.git

# 2. Go to the image directory.
$ cd pyodbc/images/pyodbc

# 3. Build docker image.
$ make build

# 4. Run the container
$ docker run laudio/pyodbc:<tag>
```

## Testing

You can build the test container image providing the flag `--target=test` and run it.

```bash
# Create .env.test file with your database connection creds
# using the the example file .env.example.
# You'll need to update .env.test with your values after this.
$ cp .env.example .env.test

# Build the test container image and run tests.
$ make clean build test
```

## Examples

### Basic Connections

Examples showing a basic use case.

1. [MSSQL Example](examples/app-mssql)
2. [PostgreSQL Example](examples/app-pg)
3. [MySQL Example](examples/app-mysql)

### Data Pipelines

Examples illustrating data pipelines using pyodbc.

1. [Data Transfer Example (PostgreSQL)](examples/data-transfer-pg)
2. [Data Transfer Example (MSSQL)](examples/data-transfer-mssql)
3. [Data Transfer Example (MySQL)](examples/data-transfer-mysql)

## License

Licensed under [MIT](LICENSE).
