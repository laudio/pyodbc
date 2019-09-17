# pyodbc

[![Travis](https://img.shields.io/travis/com/laudio/pyodbc.svg?style=flat-square&branch=master)](https://travis-ci.com/laudio/pyodbc)
[![LICENSE](https://img.shields.io/github/license/laudio/pyodbc.svg?style=flat-square)](https://github.com/laudio/pyodbc/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/laudio/pyodbc)

Docker image with python 3.7 and [pyodbc](https://github.com/mkleehammer/pyodbc), includes odbc drivers for MSSQL and PostgreSQL.

https://hub.docker.com/r/laudio/pyodbc

## Usage

```bash
$ docker pull laudio/pyodbc
```

## Development

```bash
# 1. Clone this repository.
$ git clone git@github.com:laudio/pyodbc.git

# 2. Go to the cloned path.
$ cd pyodbc

# 3. Build a docker image.
$ docker build --target=base -t laudio/pyodbc:<tag> .

# 4. Run the container
$ docker run laudio/pyodbc:<tag>
```

## Testing

You can build the test container image providing the flag `--target=test` and run it.

```bash
# Build the test container image
$ docker build --target=test laudio/pyodbc:test .

# Run tests
$ docker run laudio/pyodbc:test
```

## License

Licensed under [MIT](LICENSE).
