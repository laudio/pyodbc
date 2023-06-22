''' Tests for database connections. '''

from util import exec_pyodbc_query, exec_sqlcmd_query, PG, MSSQL_17, MSSQL_18


def test_pyodbc_mssql():
    ''' Test connection to MSSQL Server. '''
    result1 = exec_pyodbc_query(MSSQL_17, "SELECT 'It works!'")
    result2 = exec_pyodbc_query(MSSQL_18, "SELECT 'It works!'")

    assert result1 == 'It works!'
    assert result2 == 'It works!'

def test_pyodbc_pg():
    ''' Test connection to PostgreSQL Server. '''
    result = exec_pyodbc_query(PG, "SELECT 'It works!'")

    assert result == 'It works!'


def test_sqlcmd_mssql():
    ''' Test connection to MSSQL Server. '''
    result1 = exec_sqlcmd_query(MSSQL_17, "SELECT 'It works!'")
    result2 = exec_sqlcmd_query(MSSQL_18, "SELECT 'It works!'")

    assert 'It works' in str(result1)
    assert 'It works' in str(result2)
