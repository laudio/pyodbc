''' Tests for MSSQL. '''
from util import exec_query, MSSQL


def test_connection():
    ''' Test connection to MSSQL Server using Microsoft ODBC Driver. '''
    result = exec_query(MSSQL, "SELECT 'It works!'")

    assert result == 'It works!'
