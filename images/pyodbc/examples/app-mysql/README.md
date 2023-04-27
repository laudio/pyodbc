# MySQL Example

Example project using mysql with pyodbc docker image.

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
app_1    | Establishing mysql database connection.
app_1    | Create a new table for users.
app_1    | Populate users data.
app_1    | List of data.
app_1    | ID    NAME            CITY
app_1    | --------------------------------
app_1    | 1     Laura Levy      Evanberg
app_1    | 2     Justin James    Caseyport
app_1    | 3     Peggy Joseph    Baker Haven
app_1    | Closing the connection.
```
