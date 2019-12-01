''' Utilities for test. '''

import os
from typing import Dict
import pyodbc
from pyodbc import Connection
from typing import List
from logging import getLogger, basicConfig, DEBUG

basicConfig(level='DEBUG')
logger: str = getLogger()

# Database Connections
PG: str = 'pg'
MSSQL: str = 'mssql'

# Database Drivers
drivers: Dict[str] = {}
drivers[PG] = '{PostgreSQL Unicode}'
drivers[MSSQL] = '{ODBC Driver 17 for SQL Server}'


def get_conn_str(db: str) -> str:
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

    else:
        raise RuntimeError('Unsupported database connection: {}'.format(db))


def connect(driver: str) -> Connection:
    ''' Connect to the database server. '''
    connection_str = get_conn_str(driver)

    logger.debug('Connecting to Database Server [driver={}].'.format(driver))

    return pyodbc.connect(connection_str)


def exec_query(db: str, sql: str) -> List:
    ''' Execute a test SQL query on the given database. '''
    connection = connect(db)

    logger.debug('Connection estabilished with database - {}.'.format(db))
    logger.debug('Creating a new cursor.')
    cursor = connection.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchall()
    logger.debug('Received result set.')

    return result
