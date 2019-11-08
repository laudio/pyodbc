''' Main module. '''
import sys
import os
import time
import pyodbc

CONNECTION_STRING = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'


def connect_db():
    ''' Connect to database. '''
    print('Establishing mssql database connection.')
    connection_str = CONNECTION_STRING.format(
        server=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        username=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )

    return pyodbc.connect(connection_str, timeout=300)


def setup_table(cur):
    ''' Create table and populate data. '''
    print('Create a new table for fruits.')
    cur.execute('CREATE TABLE fruits (id INT, name NVARCHAR(50), quantity INT)')
    conn.commit()

    print('Populate fruits data.')
    cur.execute('INSERT INTO fruits VALUES (1, ?, ?)', ('Banana', 150))
    cur.execute('INSERT INTO fruits VALUES (2, ?, ?)', ('Orange', 64))
    cur.execute('INSERT INTO fruits VALUES (3, ?, ?)', ('Apple', 35))
    conn.commit()


def fetch_data(cur):
    ''' Fetch all data from the table. '''
    print('List of data.')
    cur.execute('SELECT * FROM fruits')

    return cur.fetchall()


def display_data(rows):
    ''' Print rows in the console. '''
    template = '{:<5} {:<15} {:<10}'
    print(template.format('ID', 'NAME', 'QUANTITY'))
    print('-' * 32)
    for row in rows:
        print(template.format(row.id, row.name, row.quantity))


def main():
    ''' App entrypoint. '''
    time.sleep(5)  # Wait for mssql database server to fully spawn.
    conn = connect_db()
    cur = conn.cursor()

    setup_table(cur)
    rows = fetch_data(cur)
    display_data(rows)

    print('Closing the connection.')
    cur.close()
    conn.close()
    sys.exit(0)


main()
