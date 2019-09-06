''' Tests for database connections. '''

from util import mssql_exec_query, pg_exec_query


def test_mssql():
    ''' Test connection to MSSQL Server. '''
    result = mssql_exec_query("SELECT 'It works!'")

    assert result == 'It works!'


def test_pg():
    ''' Test connection to PostgreSQL Server. '''
    result = pg_exec_query("SELECT 'It works!'")

    assert result == 'It works!'
