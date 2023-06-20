[![Travis](https://img.shields.io/travis/com/laudio/pyodbc.svg?style=flat-square&branch=master)](https://travis-ci.com/laudio/pyodbc)
[![LICENSE](https://img.shields.io/github/license/laudio/pyodbc.svg?style=flat-square)](https://github.com/laudio/pyodbc/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/laudio/pyodbc)

Docker image with python 3.11 and [pyodbc](https://github.com/mkleehammer/pyodbc). Includes ODBC drivers for MSSQL, PostgreSQL and MySQL.

https://hub.docker.com/r/laudio/pyodbc

## Images

| Image                                 | Description                                                               |
| ------------------------------------- | ------------------------------------------------------------------------- |
| [pyodbc](images/pyodbc)               | Python 3.11 with pyodbc and ODBC drivers for MSSQL, PostgreSQL and MySQL. |
| [pyodbc-sqlcmd](images/pyodbc-sqlcmd) | Alternative image which includes laudio/pyodbc and sqlcmd util.           |

Take a look at examples in the [examples](images/pyodbc/examples) directory.

## License

Licensed under [MIT](LICENSE).
