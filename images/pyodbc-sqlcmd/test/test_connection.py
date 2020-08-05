''' Tests for database connections. '''

from util import exec_pyodbc_query, exec_sqlcmd_query, PG, MSSQL


def test_pyodbc_mssql():
    ''' Test connection to MSSQL Server. '''
    result = exec_pyodbc_query(MSSQL, "SELECT 'It works!'")

    assert result == 'It works!'


def test_pyodbc_pg():
    ''' Test connection to PostgreSQL Server. '''
    result = exec_pyodbc_query(PG, "SELECT 'It works!'")

    assert result == 'It works!'


def test_sqlcmd():
    ''' Test connection to MSSQL Server. '''
    result = exec_sqlcmd_query("SELECT 'It works!'")

    assert result == b'         \n---------\nIt works!\n\n(1 rows affected)\n'
