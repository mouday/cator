# -*- coding: utf-8 -*-

try:
    # pymysql
    # https://pypi.org/project/pymysql/
    # https://pymysql.readthedocs.io/en/latest/
    from pymysql import connect
    from pymysql.err import OperationalError

except ImportError:
    # mysql-connector-python https://dev.mysql.com/doc/connector-python/en/
    try:
        from mysql.connector import connect
        from mysql.connector.errors import OperationalError
    except ImportError:
        try:
            # mysqlclient https://mysqlclient.readthedocs.io/index.html
            from MySQLdb import connect
            from MySQLdb import OperationalError
        except ImportError:
            from cator.common import connect, OperationalError

from cator.base.database import DatabaseProxy
from cator.base.reconnect_mixin import ReconnectMixin
from cator.logger import logger


class MysqlDatabaseProxy(DatabaseProxy):
    """
    doc:
    mysql-connector-python: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    pymysql: https://pymysql.readthedocs.io/
    """

    def connect(self):
        logger.debug("Database open")
        return connect(**self.config)


class MysqlReconnectDatabaseProxy(ReconnectMixin, MysqlDatabaseProxy):
    reconnect_errors = (
        # pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')
        "(2013, 'lost connection to mysql server during query')",
        # mysql.connector.errors.OperationalError: MySQL Connection not available
        "mysql connection not available",
        # MySQLdb.OperationalError: (4031, 'The client was disconnected by the server because of inactivity. See wait_timeout and interactive_timeout for configuring this behavior.')
        "(4031, 'the client was disconnected by the server because of inactivity. see wait_timeout and interactive_timeout for configuring this behavior.')"
    )

    def is_reconnect_error(self, error):

        if isinstance(error, OperationalError):
            if str(error).lower() in self.reconnect_errors:
                return True

        return False
