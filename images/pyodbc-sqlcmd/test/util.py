''' Utilities for test. '''

import os
import pyodbc
import subprocess

from logging import getLogger, basicConfig

basicConfig(level='DEBUG')
logger = getLogger()

# Database Connections
PG = 'pg'
MSSQL_17: str = 'mssql_17'
MSSQL_18: str = 'mssql_18'

# Database Drivers
drivers = {}
drivers[PG] = '{PostgreSQL Unicode}'
drivers[MSSQL_17] = '{ODBC Driver 17 for SQL Server}'
drivers[MSSQL_18] = '{ODBC Driver 18 for SQL Server}'
conn_str = ';'.join([
    'DRIVER={driver}',
    'SERVER={server}',
    'PORT={port}',
    'DATABASE={database}',
    'UID={username}',
    'PWD={password}',
    'TrustServerCertificate=yes'

])


def get_db_config(db):
    ''' Get database connection string for the provided driver. '''
    driver = drivers[db]

    if db == PG:
        return {
            "driver": driver,
            "server": os.environ['TEST_PG_DB_HOST'],
            "database": os.environ['TEST_PG_DB_NAME'],
            "username": os.environ['TEST_PG_DB_USER'],
            "password": os.environ['TEST_PG_DB_PASSWORD'],
            "port": 5432
        }

    elif db == MSSQL_17:
        return {
            "driver": driver,
            "server": os.environ['TEST_MSSQL_DB_HOST'],
            "database": os.environ['TEST_MSSQL_DB_NAME'],
            "username": os.environ['TEST_MSSQL_DB_USER'],
            "password": os.environ['TEST_MSSQL_DB_PASSWORD'],
            "port": 1433
        }
    
    elif db == MSSQL_18:
        return {
            "driver": driver,
            "server": os.environ['TEST_MSSQL_DB_HOST'],
            "database": os.environ['TEST_MSSQL_DB_NAME'],
            "username": os.environ['TEST_MSSQL_DB_USER'],
            "password": os.environ['TEST_MSSQL_DB_PASSWORD'],
            "port": 1433,
        }
    else:
        raise RuntimeError('Unsupported database connection: {}'.format(db))


def connect_pyodbc(driver):
    ''' Connect to the database server. '''
    db_config = get_db_config(driver)
    connection_str = conn_str.format(**db_config)

    logger.debug('Connecting to Database Server [driver={}].'.format(driver))

    return pyodbc.connect(connection_str)


def exec_pyodbc_query(db, sql):
    ''' Execute a test SQL query on the given database. '''
    connection = connect_pyodbc(db)

    logger.debug('Connection estabilished with database - {}.'.format(db))
    logger.debug('Creating a new cursor.')
    cursor = connection.cursor()
    logger.debug('Executing SQL query.')
    result = cursor.execute(sql).fetchval()
    logger.debug('Received result set.')

    return result


def exec_sqlcmd_query(db, sql):
    ''' Execute a test SQL query on the given database. '''
    db_config = get_db_config(db)
    
    command = (
        'sqlcmd -S $DB_SERVER,$DB_PORT -U $DB_USER -P "$DB_PASSWORD" -d $DB_DATABASE -b '
        + '-Q "{}"'.format(sql)
    )

    output = subprocess.check_output(
        command,
        shell=True,
        stderr=subprocess.STDOUT,
        env={
            **os.environ,
            "DB_SERVER": db_config.get("server"),
            "DB_DATABASE": db_config.get("database"),
            "DB_USER": db_config.get("username"),
            "DB_PORT": str(db_config.get("port")),
            "DB_PASSWORD": db_config.get("password"),
        }
    )

    return output
