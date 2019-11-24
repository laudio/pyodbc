''' Main module. '''
import sys
import os
import time
import pyodbc
from faker import Faker
from typing import List, Tuple


CONNECTION_STRING = 'DRIVER={{PostgreSQL Unicode}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
RECORD_COUNT = 10000
SQL_INSERT_DATA = 'INSERT INTO users (id, name, city) VALUES ({id}, {name}, {city});'


def main():
    ''' App entrypoint. '''
    # Wait for postgres database server to fully spawn.
    time.sleep(5)

    source_db_conn, dest_db_conn = connect_to_databases()
    data = get_data(RECORD_COUNT)
    load_data  = insert_source_db(data)

    with source_db_conn, dest_db_conn:

        source_db_cur = source_db_conn.cursor()
        dest_db_cur = dest_db_conn.cursor()

        with source_db_cur, dest_db_cur:

            print(f'Create users table and populate data in source database.')
            source_db_cur.execute(extract_sql('sql/source_db_setup.sql'))
            source_db_conn.commit()

            print(f'Create users table in destination database.')
            dest_db_cur.execute(extract_sql('sql/dest_db_setup.sql'))
            dest_db_conn.commit()

            transfer_data(source_db_cur, dest_db_cur, dest_db_conn)

            print(f'Display users data in destination database.')
            display_users(dest_db_cur)


def get_connection(host: str, db_name: str, db_user: str, db_password: str): 
    ''' Initiates and returns connection of a database.'''
    print(f'Establishing postgres database connection to {host}.')
    connection_str = CONNECTION_STRING.format(
        server=host,
        database=db_name,
        username=db_user,
        password=db_password
    )
    return pyodbc.connect(connection_str, timeout=300);


def connect_to_databases():
    ''' Extracts databases credentials from the environment and returns their connections.'''
    source_db_conn = get_connection(
            os.environ['DB1_HOST'], 
            os.environ['DB1_NAME'], 
            os.environ['DB1_USERNAME'], 
            os.environ['DB1_PASSWORD']
        )

    dest_db_conn = get_connection(
            os.environ['DB2_HOST'], 
            os.environ['DB2_NAME'],
            os.environ['DB2_USERNAME'], 
            os.environ['DB2_PASSWORD']
        )

    return source_db_conn, dest_db_conn


def get_data(count: int) -> List[Tuple]:
    ''' Generate user data. '''
    fake = Faker()
    row = lambda n: (n + 1, repr(fake.name()), repr(fake.city()))

    return [row(i) for i in range(count)]


def insert_source_db(data):
    for i in data: 
        with open('sql/source_db_setup.sql', 'a') as file:
            file.write(SQL_INSERT_DATA.format(
            id = i[0], 
            name = i[1], 
            city = i[2]
        )+ '\n')


def extract_sql(file: str):
    ''' Reads an SQL file and returns it's contents.'''
    with open (file, 'rt') as file:
        contents = file.read()  

    return contents


def transfer_data(source_db_cursor, dest_db_cursor, dest_db_conn):
    ''' Extracts users data from source database and stores them in destination database.'''
    print(f'Extracting users data from source database.')
    source_db_cursor.execute('SELECT * FROM users')
    rows = source_db_cursor.fetchall()

    print(f'Transferring users data to destination database.')
    for row in rows:
        dest_db_cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (row.id, row.name, row.city))
    dest_db_conn.commit()
    
    print(f"Transferred {len(rows)} rows of users data from source database to destination database.")


def display_users(db_cursor):
    ''' Displays users data. '''
    db_cursor.execute('SELECT * FROM users')
    transfered_data = db_cursor.fetchall()
    template = '{:<5} {:<15} {:<10}'

    print(template.format('ID', 'NAME', 'CITY'))
    print('-' * 32)

    for row in transfered_data:
        print(template.format(row.id, row.name, row.city))


if __name__ == '__main__':
    main()
    sys.exit(0)
