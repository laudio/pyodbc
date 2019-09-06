''' Test MSSQL Connection works. '''

from util import logger, mssql_exec_query


def test_mssql():
    ''' Test connection to MSSQL Server. '''
    logger.debug('Starting to connect')
    result = mssql_exec_query("SELECT 'It works!'")

    assert result == 'It works!'
