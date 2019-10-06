# MSSQL Example
Example project using mssql with pyodbc docker image.

### Usage

- Set credentials for the DB in enviromental variables.
```                                                                      
export DB_NAME='tempdb';
export DB_USERNAME='SA';
export DB_PASSWORD='someP4ssword';
```
- Start the containers

```
docker-compose up
```
