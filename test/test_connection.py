''' Tests for database connections. '''

from util import exec_query, PG, MSSQL, MYSQL


def test_mssql():
    ''' Test connection to MSSQL Server. '''
    result = exec_query(MSSQL, "SELECT 'It works!'")

    assert result == 'It works!'


def test_pg():
    ''' Test connection to PostgreSQL Server. '''
    result = exec_query(PG, "SELECT 'It works!'")

    assert result == 'It works!'


def test_mysql():
    ''' Test connection to MySQL Server. '''
    result = exec_query(MYSQL, "SELECT 'It works!'")

    assert result == 'It works!'
