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

    # Source
    print('Establishing mssql database connection to source db')
    source_connection_str = CONNECTION_STRING.format(
        server=os.environ['SOURCE_DB_HOST'],
        database=os.environ['DB_NAME'],
        username=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    
    source_conn = pyodbc.connect(source_connection_str, timeout=300)
    cur1 = source_conn.cursor()

    print('Create a new table for fruits.')
    cur1.execute('CREATE TABLE fruits (id INT, name NVARCHAR(50), quantity INT)')
    source_conn.commit()


    print('Populate fruits data.')
    cur1.execute('INSERT INTO fruits VALUES (1, ?, ?)', ('Banana', 150))
    cur1.execute('INSERT INTO fruits VALUES (2, ?, ?)', ('Orange', 64))
    cur1.execute('INSERT INTO fruits VALUES (3, ?, ?)', ('Apple', 35))
    source_conn.commit()

    print('---selecting data from source db----')
    cur1.execute('SELECT * FROM fruits')
    source_rows = cur1.fetchall()
    
    print('---closing source db----')
    cur1.close()
    source_conn.close()


    # Destination
    print('Establishing mssql database connection to destination db')
  
    destination_connection_str = CONNECTION_STRING.format(
        server=os.environ['DESTINATION_DB_HOST'],
        database=os.environ['DB_NAME'],
        username=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )

    destination_conn = pyodbc.connect(destination_connection_str, timeout=300)
    cur2 = destination_conn.cursor()

    print('\n\n\nCreate a new table for fruits_backup. on destination db')

    cur2.execute('CREATE TABLE fruits_backup (id INT, name NVARCHAR(50), quantity INT)')
    destination_conn.commit()


    print('Inserting data to destination db')
    for row_data in source_rows:
        cur2.execute('INSERT INTO fruits_backup VALUES (?, ?, ?)', (row_data.id,row_data.name,row_data.quantity))
        destination_conn.commit()

    cur2.execute('SELECT * FROM fruits_backup')
    destination_rows = cur2.fetchall()

    print('----------------List of data from destination.-----------------------')
    template = '{:<5} {:<15} {:<10}'
    print(template.format('ID', 'NAME', 'QUANTITY'))
    print('-' * 32)
    for row in destination_rows:
        print(template.format(row.id, row.name, row.quantity))

    print('--- Closing the destination db ---.')
    cur2.close()
    destination_conn.close()

    sys.exit(0)


main()
