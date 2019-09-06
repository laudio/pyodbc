''' Test MSSQL Connection works. '''

import os
import pyodbc

from logging import getLogger, basicConfig, DEBUG

basicConfig(level='DEBUG')
logger = getLogger()

ODBC_DRIVER = '{ODBC Driver 17 for SQL Server}'
CONNECTION_STRING = 'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'


def main():
    ''' Lambda function handler. '''
    logger.debug('Starting to connect')
    result = exec_db_query("SELECT 'Hello World!'")

    print(result)


def exec_db_query(sql):
    ''' Execute a test SQL query on the database. '''
    connection_str = CONNECTION_STRING.format(
        driver=ODBC_DRIVER,
        server=os.environ['MSSQL_DB_HOST'],
        database=os.environ['MSSQL_DB_NAME'],
        username=os.environ['MSSQL_DB_USER'],
        password=os.environ['MSSQL_DB_PASSWORD'],
        port=1433
    )

    logger.debug('Connecting to MSSQL Server.')
    cnxn = pyodbc.connect(connection_str)
    logger.debug('MSSQL Database connection estabilished.')
    cursor = cnxn.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received SQL query result.')

    return result


main()
