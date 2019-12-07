''' Main module. '''
import os
import sys
import time
from dotenv import load_dotenv

import pyodbc
from faker import Faker

load_dotenv()

CONNECTION_STR: str = 'DRIVER={{MySQL ODBC 8.0 Driver}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

SQL_CREATE_TABLE: str = '''
    CREATE TABLE users (
        id INT, 
        name VARCHAR(50), 
        city VARCHAR(50)
    )
'''

SQL_INSERT_DATA: str = 'INSERT into users (id, name, city) VALUES (?, ?, ?)'

RECORD_COUNT: int = 10000


def get_data(count):
    ''' Generate user data. '''
    fake = Faker()
    row = lambda n: (n + 1, fake.format('name'), fake.format('city'))

    return [row(i) for i in range(count)]

def connect_db(): 
    ''' Connect to database. '''
    print('Establishing mysql database connection.')
    connection_str = CONNECTION_STR.format(
        server=os.getenv('DB_HOST'), 
        database=os.getenv('DB_NAME'), 
        username=os.getenv('DB_USERNAME'), 
        password=os.getenv('DB_PASSWORD')
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
    cur.execute('SELECT * from users;') 

    return cur.fetchall()

def display_data(rows): 
    template = '{:<5} {:<15} {:<10}'
    print(template.format('ID', 'NAME', 'CITY'))
    print('-' * 32)

    for row in rows: 
        print(template.format(row.id, row.name, row.city))

def main(): 
    ''' App entrypoint. '''
    time.sleep(5) # wait for mysql database to fully spawn. 
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
    
        

