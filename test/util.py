''' Utilities for test. '''
import os
from typing import Dict, List
from logging import getLogger, basicConfig, Logger

import pyodbc


basicConfig(level='DEBUG')
logger: Logger = getLogger()

# Database Connections
PG: str = 'pg'
MYSQL: str = 'mysql'
MSSQL: str = 'mssql_18'

# Connection strings
CONN_STR: str = ';'.join([
    'DRIVER={driver}',
    'SERVER={server}',
    'PORT={port}',
    'DATABASE={database}',
    'UID={username}',
    'PWD={password}',
    'TrustServerCertificate=yes'
])

constr: Dict = {}
constr[PG] = lambda: CONN_STR.format(
    driver='{PostgreSQL Unicode}',
    port=5432,
    server=os.environ['TEST_POSTGRESQL_DB_HOST'],
    database=os.environ['TEST_POSTGRESQL_DB_NAME'],
    username=os.environ['TEST_POSTGRESQL_DB_USER'],
    password=os.environ['TEST_POSTGRESQL_DB_PASSWORD']
)

constr[MSSQL] = lambda: CONN_STR.format(
    driver='{ODBC Driver 18 for SQL Server}',
    port=1433,
    server=os.environ['TEST_MSSQL_DB_HOST'],
    database=os.environ['TEST_MSSQL_DB_NAME'],
    username=os.environ['TEST_MSSQL_DB_USER'],
    password=os.environ['TEST_MSSQL_DB_PASSWORD'],
)

constr[MYSQL] = lambda: CONN_STR.format(
    driver='{MySQL ODBC 8.3 Unicode Driver}',
    port=3306,
    server=os.environ['TEST_MYSQL_DB_HOST'],
    database=os.environ['TEST_MYSQL_DB_NAME'],
    username=os.environ['TEST_MYSQL_DB_USER'],
    password=os.environ['TEST_MYSQL_DB_PASSWORD']
)

def connect(db: str) -> pyodbc.Connection:
    ''' Connect to the database server. '''
    if not constr.get(db):
        raise RuntimeError('Unsupported database connection: {}'.format(db))

    connection_str = constr[db]()

    logger.debug('Connecting to database server [{}].'.format(db))

    return pyodbc.connect(connection_str)

def exec_query(db: str, sql: str) -> List:
    ''' Execute a test SQL query on the given database. '''
    connection = connect(db)

    logger.debug('Connection established with database - {}.'.format(db))
    logger.debug('Creating a new cursor.')
    cursor = connection.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received result set.')

    return result
