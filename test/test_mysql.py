''' Tests for MySQL. '''
from util import exec_query, MYSQL


def test_connection():
    ''' Test connection to MySQL Server. '''
    result = exec_query(MYSQL, "SELECT 'It works!'")

    assert result == 'It works!'
