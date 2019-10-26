''' Main module. '''
import sys
import os
import time
import pyodbc

CONNECTION_STRING = 'DRIVER={{PostgreSQL Unicode}};SERVER={server};DATABASE={database};UID={username};PWD={password};'


def main():
    ''' App entrypoint. '''
    # Wait for postgres database server to fully spawn.
    time.sleep(5)

    db1_name = os.environ['DB1_NAME']
    db1_conn = get_connection(
            os.environ['DB1_HOST'], 
            db1_name, 
            os.environ['DB1_USERNAME'], 
            os.environ['DB1_PASSWORD']
        )
    db1_cur = db1_conn.cursor()

    db2_name = os.environ['DB2_NAME']
    db2_conn = get_connection(
            os.environ['DB2_HOST'], 
            db2_name,
            os.environ['DB2_USERNAME'], 
            os.environ['DB2_PASSWORD']
        )
    db2_cur = db2_conn.cursor()

    print(f'Creating fruits table and populating data in {db1_name}.')
    db1_cur.execute(extract_sql('sql/db1_setup.sql'))
    db1_cur.execute('INSERT INTO fruits VALUES (1, ?, ?)', ('Banana', 150))
    db1_cur.execute('INSERT INTO fruits VALUES (2, ?, ?)', ('Orange', 64))
    db1_cur.execute('INSERT INTO fruits VALUES (3, ?, ?)', ('Apple', 35))
    db1_conn.commit()

    print(f'Create fruits table in {db2_name} database.')
    db2_cur.execute(extract_sql('sql/db2_setup.sql'))
    db2_conn.commit()

    print(f'Extracting fruits data from {db1_name} database.')
    db1_cur.execute('SELECT * FROM fruits')
    rows = db1_cur.fetchall()

    print(f'Transferring fruits data to {db2_name} database.')
    for row in rows:
        db2_cur.execute('INSERT INTO fruits VALUES (?, ?, ?)', (row.id, row.name, row.quantity))
    db2_conn.commit()

    db2_cur.execute('SELECT * FROM fruits')
    transfered_data = db2_cur.fetchall()
    template = '{:<5} {:<15} {:<10}'

    print(f'Fruits data in {db2_name} database.')
    print(template.format('ID', 'NAME', 'QUANTITY'))
    print('-' * 32)

    for row in transfered_data:
        print(template.format(row.id, row.name, row.quantity))

    print('Closing connections.')
    db1_cur.close()
    db1_conn.close()

    db2_cur.close()
    db2_conn.close()


def get_connection(host: str, db_name: str, db_user: str, db_password: str): 
    print(f'Establishing postgres database connection to {host},')
    connection_str = CONNECTION_STRING.format(
        server=host,
        database=db_name,
        username=db_user,
        password=db_password
    )
    return pyodbc.connect(connection_str, timeout=300);


def extract_sql(file: str):
    with open (file, 'rt') as file:
        contents = file.read()  
    return contents


if __name__ == '__main__':
    main()
    sys.exit(0)
