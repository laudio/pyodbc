# PostgreSQL Data Transfer Example

Example project using postgres with pyodbc docker image.

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
app_1           | Establishing postgres database connection to postgres-db1.
app_1           | Establishing postgres database connection to postgres-db2.
app_1           | Create fruits table and populate data in source database.
app_1           | Create fruits table in destination database.
app_1           | Extracting fruits data from source database.
app_1           | Transferring fruits data to destination database.
app_1           | Display fruits data in destination database.
app_1           | ID    NAME            QUANTITY  
app_1           | --------------------------------
app_1           | 1     Banana          150       
app_1           | 2     Orange          64        
app_1           | 3     Apple           35        
```
