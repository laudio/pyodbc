''' Main module. '''
import sys
import os
import time
import pyodbc

CONNECTION_STRING = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'


def main():
    ''' App entrypoint. '''
    # Wait for mssql db server to fully spawn.
    time.sleep(5)

    print("Establishing mssql database connection")
    connection_str = CONNECTION_STRING.format(
        server=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        username=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    conn = pyodbc.connect(connection_str, timeout=300)
    cur = conn.cursor()

    print("Create a new table: fruits")
    cur.execute("CREATE TABLE fruits (id INT, name NVARCHAR(50), quantity INT);")
    conn.commit()

    print("Insert data into `fruits` table")
    cur.execute("INSERT INTO fruits VALUES (1, 'banana', 150);")
    cur.execute("INSERT INTO fruits VALUES (2, 'orange', 64);")
    cur.execute("INSERT INTO fruits VALUES (2, 'apples', 35);")
    conn.commit()

    print("Select data from `fruits` table")
    cur.execute("SELECT * FROM fruits WHERE quantity > 50;")
    rows = cur.fetchall()
    for row in rows:
        print(row.id, row.name, row.quantity)

    print("Closing the connection")
    cur.close()
    conn.close()

    sys.exit(0)


main()
