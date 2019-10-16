# MSSQL Example

Example project using mssql with pyodbc docker image.

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

```bash
app_1    | Establishing mssql database connection.
app_1    | Create a new table for fruits.
app_1    | Populate fruits data.
app_1    | List of data.
app_1    | ID    NAME            QUANTITY
app_1    | --------------------------------
app_1    | 1     Banana          150
app_1    | 2     Orange          64
app_1    | 3     Apple           35
app_1    | Closing the connection.
```
