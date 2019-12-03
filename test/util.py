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

# Connection strings
CONN_STR = ';'.join([
    'DRIVER={driver}',
    'SERVER={server}',
    'PORT={port}',
    'DATABASE={database}',
    'UID={username}',
    'PWD={password}'
])

constr = {}
constr[PG] = lambda: CONN_STR.format(
    driver='{PostgreSQL Unicode}',
    server=os.environ['TEST_PG_DB_HOST'],
    database=os.environ['TEST_PG_DB_NAME'],
    username=os.environ['TEST_PG_DB_USER'],
    password=os.environ['TEST_PG_DB_PASSWORD'],
    port=5432
)
constr[MSSQL] = lambda: CONN_STR.format(
    driver='{ODBC Driver 17 for SQL Server}',
    server=os.environ['TEST_MSSQL_DB_HOST'],
    database=os.environ['TEST_MSSQL_DB_NAME'],
    username=os.environ['TEST_MSSQL_DB_USER'],
    password=os.environ['TEST_MSSQL_DB_PASSWORD'],
    port=1433
)
constr[MYSQL] = lambda: CONN_STR.format(
    driver='{MySQL ODBC 8.0 Driver}',
    server=os.environ['TEST_MYSQL_DB_HOST'],
    database=os.environ['TEST_MYSQL_DB_NAME'],
    username=os.environ['TEST_MYSQL_DB_USER'],
    password=os.environ['TEST_MYSQL_DB_PASSWORD'],
    port=3306
)


def connect(db):
    ''' Connect to the database server. '''
    if not constr.get(db):
        raise RuntimeError('Unsupported database connection: {}'.format(db))

    connection_str = constr[db]()

    logger.debug('Connecting to database server [{}].'.format(db))

    return pyodbc.connect(connection_str)


def exec_query(db, sql):
    ''' Execute a test SQL query on the given database. '''
    connection = connect(db)

    logger.debug('Connection established with database - {}.'.format(db))
    logger.debug('Creating a new cursor.')
    cursor = connection.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received result set.')

    return result
