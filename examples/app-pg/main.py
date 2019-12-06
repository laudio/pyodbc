''' Main module. '''
import sys
import os
import time
import pyodbc
from faker import Faker
from typing import List, Tuple


CONNECTION_STRING = 'DRIVER={{PostgreSQL Unicode}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

SQL_CREATE_TABLE = '''
    CREATE TABLE users (
        id INT,
        name VARCHAR(50),
        city VARCHAR(50)
    )
'''

SQL_INSERT_DATA = 'INSERT INTO users (id, name, city) VALUES (?, ?, ?)'

RECORD_COUNT = 10000


def get_data(count: int) -> List[Tuple]:
    ''' Generate user data. '''
    fake = Faker()
    row = lambda n: (n + 1, fake.format('name'), fake.format('city'))

    return [row(i) for i in range(count)]


def connect_db():
    ''' Connect to database. '''
    print('Establishing pg database connection.')
    connection_str = CONNECTION_STRING.format(
        server=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        username=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )

    return pyodbc.connect(connection_str, timeout=300)


def setup_table(cur, data):
    ''' Create table and populate data. '''
    print('Create a new table for users.')
    cur.execute(SQL_CREATE_TABLE)
    cur.commit()

    print('Populate users data.')
    for row in data:
        cur.execute(SQL_INSERT_DATA, row)
    cur.commit()


def fetch_data(cur):
    ''' Fetch all data from the table. '''
    print('List of data.')
    cur.execute('SELECT * FROM users')

    return cur.fetchall()


def display_data(rows):
    ''' Print rows in the console. '''
    template = '{:<5} {:<15} {:<10}'
    print(template.format('ID', 'NAME', 'CITY'))
    print('-' * 32)
    for row in rows:
        print(template.format(row.id, row.name, row.city))


def main():
    ''' App entrypoint. '''
    time.sleep(5)  # Wait for database server to fully spawn.
    conn = connect_db()
    cur = conn.cursor()
    data = get_data(RECORD_COUNT)

    setup_table(cur, data)
    rows = fetch_data(cur)
    display_data(rows)

    print('Closing the connection.')
    cur.close()
    conn.close()
    sys.exit(0)


main()
