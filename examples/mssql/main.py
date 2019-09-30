import pyodbc
import sys
import time

# waiting for mssql db server to fully spawn
time.sleep(3)

print("Creating a mssql connection")
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=mssql_server;DATABASE=tempdb;UID=SA;PWD=bad_P4ssword;')
cur = conn.cursor()


print("Create a new table: Fruits")
cur.execute("CREATE TABLE Fruits (id INT, name NVARCHAR(50), quantity INT);")
conn.commit()

print("Insert data into `Fruits` table")
cur.execute("INSERT INTO Fruits VALUES (1, 'banana', 150);")
cur.execute("INSERT INTO Fruits VALUES (2, 'orange', 64);")
cur.execute("INSERT INTO Fruits VALUES (2, 'apples', 35);")
conn.commit()

print("Select data from `Fruits` table")
cur.execute("SELECT * FROM Fruits WHERE quantity > 50;")
rows = cur.fetchall()
for row in rows:
    print(row.id, row.name, row.quantity)

print("Closing the connection")
cur.close()
conn.close()

sys.exit(0)