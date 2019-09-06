''' Utilities for test. '''

import os
import pyodbc

from logging import getLogger, basicConfig, DEBUG

basicConfig(level='DEBUG')
logger = getLogger()

PG_DRIVER = '{PostgreSQL Unicode}'
PG_CONNECTION_STRING = 'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'

MSSQL_DRIVER = '{ODBC Driver 17 for SQL Server}'
MSSQL_CONNECTION_STRING = 'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'


def get_conn_str(driver):
    ''' Get database connection string for the provided driver. '''

    if driver == PG_DRIVER:
        return PG_CONNECTION_STRING.format(
            driver=driver,
            server=os.environ['TEST_PG_DB_HOST'],
            database=os.environ['TEST_PG_DB_NAME'],
            username=os.environ['TEST_PG_DB_USER'],
            password=os.environ['TEST_PG_DB_PASSWORD'],
            port=5432
        )

    elif driver == MSSQL_DRIVER:
        return MSSQL_CONNECTION_STRING.format(
            driver=MSSQL_DRIVER,
            server=os.environ['TEST_MSSQL_DB_HOST'],
            database=os.environ['TEST_MSSQL_DB_NAME'],
            username=os.environ['TEST_MSSQL_DB_USER'],
            password=os.environ['TEST_MSSQL_DB_PASSWORD'],
            port=1433
        )

    else:
        raise RuntimeError('Unsupported driver provided: {}'.format(driver))


def connect(driver):
    ''' Connect to the database server. '''
    connection_str = get_conn_str(driver)

    logger.debug('Connecting to Database Server [driver={}].'.format(driver))

    return pyodbc.connect(connection_str)


def mssql_exec_query(sql):
    ''' MSSQL - Execute a test SQL query on the database. '''
    connection = connect(MSSQL_DRIVER)

    logger.debug('MSSQL Database connection estabilished.')
    logger.debug('Creating a new cursor.')
    cursor = connection.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received SQL query result.')

    return result


def pg_exec_query(sql):
    ''' PostgreSQL - Execute a test SQL query on the database. '''
    connection = connect(PG_DRIVER)

    logger.debug('Postgresql Database connection estabilished.')
    logger.debug('Creating a new cursor.')
    cursor = connection.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received SQL query result.')

    return result
