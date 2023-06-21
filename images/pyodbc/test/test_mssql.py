''' Tests for MSSQL. '''
from util import exec_query, MSSQL_17, MSSQL_18


def test_connection():
    ''' Test connection to MSSQL Server using Microsoft ODBC Driver 17 and 18. '''
    result1 = exec_query(MSSQL_17, "SELECT 'It works!'")
    result2 = exec_query(MSSQL_18, "SELECT 'It works!'")

    assert result1 == 'It works!'
    assert result2 == 'It works!'
