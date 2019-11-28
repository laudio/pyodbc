import sys
import os
import time
import pyodbc
from faker import Faker
from typing import Tuple, Union, List, Callable, IO
from pyodbc import Cursor, Connection


CONNECTION_STRING: str = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
RECORD_COUNT: int = 10000
SQL_INSERT_DATA: str = 'INSERT INTO users (id, name, city) VALUES (?, ?, ?);'

def main():
    ''' App entrypoint. '''
    # Wait for mssql database server to fully spawn.
    time.sleep(20)

    source_db_conn, dest_db_conn = connect_to_databases()

    with source_db_conn, dest_db_conn:
        source_db_cur = source_db_conn.cursor()
        dest_db_cur = dest_db_conn.cursor()

        with source_db_cur, dest_db_cur:
            print('Create users table and populate data in source database.')
            source_db_cur.execute(extract_sql('sql/source_db_setup.sql'))
            populate_data(RECORD_COUNT, source_db_cur)
            source_db_conn.commit()

            print('Create users table in destination database.')
            dest_db_cur.execute(extract_sql('sql/dest_db_setup.sql'))
            dest_db_conn.commit()

            transfer_data(source_db_cur, dest_db_cur, dest_db_conn)

            print('Display users data of destination database.')
            display_users(dest_db_cur)


def connect_to_databases() -> Tuple:
    ''' Extracts databases credentials from the environment and returns their connections. '''
    source_db_conn = get_connection(
        os.environ['SOURCE_DB_HOST'],
        os.environ['SOURCE_DB_NAME'],
        os.environ['SOURCE_DB_USERNAME'],
        os.environ['SOURCE_DB_PASSWORD']
    )

    dest_db_conn = get_connection(
        os.environ['DESTINATION_DB_HOST'],
        os.environ['DESTINATION_DB_NAME'],
        os.environ['DESTINATION_DB_USERNAME'],
        os.environ['DESTINATION_DB_PASSWORD']
    )

    return source_db_conn, dest_db_conn


def get_connection(db_host: str, db_name: str, db_username: str, db_password: str) -> IO:
    ''' Create database connection and returns connection. '''
    connection_str = CONNECTION_STRING.format(
        server=db_host,
        database=db_name,
        username=db_username,
        password=db_password
    )

    return pyodbc.connect(connection_str, timeout=300)


def populate_data(RECORD_COUNT: int, db_cursor: Cursor) -> None:
    ''' Generate user data. '''
    fake = Faker()
    row = lambda n: (n + 1, repr(fake.name()), repr(fake.city()))

    for i in range(RECORD_COUNT):
        db_cursor.execute(SQL_INSERT_DATA, row(i))


def extract_sql(file: str):
    ''' Reads an SQL file and returns it's contents. '''
    with open(file, 'rt') as file:
        contents = file.read()

    return contents


def transfer_data(source_db_cursor: Cursor, dest_db_cursor: Cursor, dest_db_conn: Connection) -> None:
    ''' Extracts users data from source database and stores them in destination database. '''
    print('Extracting users data from source database.')
    source_db_cursor.execute('SELECT * FROM users')
    rows = source_db_cursor.fetchall()

    print('Transferring users data to destination database.')
    for row in rows:
        dest_db_cursor.execute(SQL_INSERT_DATA, (row.id, row.name, row.city))

    print(f'{len(rows)} rows transferred\n')
    dest_db_conn.commit()


def display_users(db_cursor: Cursor) -> None:
    ''' Displays users data. '''
    db_cursor.execute('SELECT * FROM users')
    transferred_data = db_cursor.fetchall()
    template = '{:<5} {:<15} {:<10}'

    print(template.format('ID', 'NAME', 'CITY'))
    print('-' * 32)

    for row in transferred_data:
        print(template.format(row.id, row.name, row.city))


if __name__ == '__main__':
    main()
    sys.exit(0)
