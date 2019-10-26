# Data Transfer for MSSQL

Example project to demonstrate a data pipeline container built using laudio/pyodbc as a base image - that transfers data from one database to another database

### Running

Create a `.env` file using the example file.

```bash
$ cp .env.example .env
```

Run the example.

```bash
$ docker-compose up
```

For changes 

```bash
$ docker-compose up --build
```

**Output**

The output of the application should look like this.

```
app_1                | Establishing mssql database connection to source db
app_1                | Create a new table for fruits.
app_1                | Populate fruits data.
app_1                | importing data from source db
app_1                | closing source db
app_1                | Establishing mssql database connection to destination db
app_1                | 
app_1                | 
app_1                | 
app_1                | Create table on the destination database.
app_1                | Transferring data into destination database.
app_1                | Data in the destination database.
app_1                | ID    NAME            QUANTITY  
app_1                | --------------------------------
app_1                | 1     Banana          150       
app_1                | 2     Orange          64        
app_1                | 3     Apple           35        
app_1                | 
app_1                | 
app_1                | 3 rows transferred
app_1                | 
app_1                | Closing the destination db.
```
