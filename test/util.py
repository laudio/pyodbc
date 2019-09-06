''' Utilities for test. '''

import os
import pyodbc

from logging import getLogger, basicConfig, DEBUG

basicConfig(level='DEBUG')
logger = getLogger()

MSSQL_ODBC_DRIVER = '{ODBC Driver 17 for SQL Server}'
MSSQL_CONNECTION_STRING = 'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'


def mssql_exec_query(sql):
    ''' Execute a test SQL query on the database. '''
    connection_str = MSSQL_CONNECTION_STRING.format(
        driver=MSSQL_ODBC_DRIVER,
        server=os.environ['TEST_MSSQL_DB_HOST'],
        database=os.environ['TEST_MSSQL_DB_NAME'],
        username=os.environ['TEST_MSSQL_DB_USER'],
        password=os.environ['TEST_MSSQL_DB_PASSWORD'],
        port=1433
    )

    logger.debug('Connecting to MSSQL Server.')
    cnxn = pyodbc.connect(connection_str)
    logger.debug('MSSQL Database connection estabilished.')
    logger.debug('Creating a new cursor.')
    cursor = cnxn.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received SQL query result.')

    return result
