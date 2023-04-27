# MSSQL Data Transfer Example

Example project to demonstrate a data pipeline container built using laudio/pyodbc as a base image - that transfers data from one mssql database to another mssql database.

### Running

Create a `.env` file using the example file.

```bash
$ cp .env.example .env
```

Run the example.

```bash
$ docker-compose up
```

**Output**

The output of the application should look like this.

```
app_1                | Create users table and populate data in source database.
app_1                | Create users table in destination database.
app_1                | Extracting users data from source database.
app_1                | Transferring users data to destination database.
app_1                |
app_1                | 3 rows transferred
app_1                |
app_1                | Display users data of destination database.
app_1                | ID    NAME            CITY
app_1                | --------------------------------
app_1                | 1     Laura Levy       Evanberg
app_1                | 2     Justin James     Caseyport
app_1                | 3     Peggy Joseph     Baker haven
```
