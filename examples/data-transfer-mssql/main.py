''' Main module. '''
import sys
import os
import time
import pyodbc

CONNECTION_STRING = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

def main():
    ''' App entrypoint. '''
    # Wait for mssql database server to fully spawn.
    time.sleep(5)

    source_db_conn, dest_db_conn = connect_to_databases()

    with source_db_conn, dest_db_conn:

        source_db_cur = source_db_conn.cursor()
        dest_db_cur = dest_db_conn.cursor()

        with source_db_cur, dest_db_cur:

            print(f'Create fruits table and populate data in source database.')
            source_db_cur.execute(extract_sql('sql/source_db_setup.sql'))
            source_db_conn.commit()

            print(f'Create fruits table in destination database.')
            dest_db_cur.execute(extract_sql('sql/dest_db_setup.sql'))
            dest_db_conn.commit()

            transfer_data(source_db_cur, dest_db_cur, dest_db_conn)

            print(f'Display fruits data of destination database.')
            display_fruits(dest_db_cur)


def connect_to_databases():
    ''' Extracts databases credentials from the environment and returns their connections.'''
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

def get_connection(db_host,db_name,db_username,db_password):

    connection_str = CONNECTION_STRING.format(
        server=db_host,
        database=db_name,
        username=db_username,
        password=db_password
    )
    
    return pyodbc.connect(connection_str, timeout=300)


def extract_sql(file: str):
    ''' Reads an SQL file and returns it's contents.'''
    with open(file, 'rt') as file:
        contents = file.read()
    return contents


def transfer_data(source_db_cursor, dest_db_cursor, dest_db_conn):
    ''' Extracts fruits data from source database and stores them in destination database.'''
    print(f'Extracting fruits data from source database.')
    source_db_cursor.execute('SELECT * FROM fruits')
    rows = source_db_cursor.fetchall()

    print(f'Transferring fruits data to destination database.')
    for row in rows:
        dest_db_cursor.execute('INSERT INTO fruits VALUES (?, ?, ?)', (row.id, row.name, row.quantity))
    
    print(f'{len(rows)} rows transferred\n')
    
    dest_db_conn.commit()


def display_fruits(db_cursor):
    ''' Displays fruits data. '''
    db_cursor.execute('SELECT * FROM fruits')
    transferred_data = db_cursor.fetchall()
    template = '{:<5} {:<15} {:<10}'

    print(template.format('ID', 'NAME', 'QUANTITY'))
    print('-' * 32)

    for row in transferred_data:
        print(template.format(row.id, row.name, row.quantity))


if __name__ == '__main__':
    main()
    sys.exit(0)
