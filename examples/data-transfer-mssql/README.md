# MSSQL Data Transfer Example

Example project to demonstrate a data pipeline container built using laudio/pyodbc as a base image - that transfers data from one mssql database to another mssql database

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
app_1                | Create fruits table and populate data in source database.
app_1                | Create fruits table in destination database.
app_1                | Extracting fruits data from source database.
app_1                | Transferring fruits data to destination database.
app_1                |
app_1                | 3 rows transferred
app_1                | 
app_1                | Display fruits data of destination database.
app_1                | ID    NAME            QUANTITY  
app_1                | --------------------------------
app_1                | 1     Banana          200       
app_1                | 2     Orange          20        
app_1                | 3     Apple           350  
```
