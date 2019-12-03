''' Utilities for test. '''

import os
import pyodbc

from logging import getLogger, basicConfig, DEBUG

basicConfig(level='DEBUG')
logger = getLogger()

# Database Connections
PG = 'pg'
MSSQL = 'mssql'
MYSQL = 'mysql'

# Database Drivers
drivers = {}
drivers[PG] = '{PostgreSQL Unicode}'
drivers[MSSQL] = '{ODBC Driver 17 for SQL Server}'
drivers[MYSQL] = '{MySQL ODBC 8.0 Driver}'


def get_conn_str(db):
    ''' Get database connection string for the provided driver. '''
    conn_str = ';'.join([
        'DRIVER={driver}',
        'SERVER={server}',
        'PORT={port}',
        'DATABASE={database}',
        'UID={username}',
        'PWD={password}'
    ])
    driver = drivers[db]

    if db == PG:
        return conn_str.format(
            driver=driver,
            server=os.environ['TEST_PG_DB_HOST'],
            database=os.environ['TEST_PG_DB_NAME'],
            username=os.environ['TEST_PG_DB_USER'],
            password=os.environ['TEST_PG_DB_PASSWORD'],
            port=5432
        )

    elif db == MSSQL:
        return conn_str.format(
            driver=driver,
            server=os.environ['TEST_MSSQL_DB_HOST'],
            database=os.environ['TEST_MSSQL_DB_NAME'],
            username=os.environ['TEST_MSSQL_DB_USER'],
            password=os.environ['TEST_MSSQL_DB_PASSWORD'],
            port=1433
        )

    elif db == MYSQL:
        return conn_str.format(
            driver=driver,
            server=os.environ['TEST_MYSQL_DB_HOST'],
            database=os.environ['TEST_MYSQL_DB_NAME'],
            username=os.environ['TEST_MYSQL_DB_USER'],
            password=os.environ['TEST_MYSQL_DB_PASSWORD'],
            port=3306
        )

    else:
        raise RuntimeError('Unsupported database connection: {}'.format(db))


def connect(driver):
    ''' Connect to the database server. '''
    connection_str = get_conn_str(driver)

    logger.debug('Connecting to Database Server [driver={}].'.format(driver))

    return pyodbc.connect(connection_str)


def exec_query(db, sql):
    ''' Execute a test SQL query on the given database. '''
    connection = connect(db)

    logger.debug('Connection estabilished with database - {}.'.format(db))
    logger.debug('Creating a new cursor.')
    cursor = connection.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received result set.')

    return result
