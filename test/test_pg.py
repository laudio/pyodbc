''' Tests for PostgreSQL. '''

from util import exec_query, PG


def test_connection():
    ''' Test connection to PostgreSQL Server. '''
    result = exec_query(PG, "SELECT 'It works!'")

    assert result == 'It works!'
