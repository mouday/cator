# -*- coding: utf-8 -*-

from cator.base import DatabaseProxy
from cator.logger import logger

try:
    from pymysql import connect
except ImportError:
    # mysql-connector-python
    try:
        from mysql.connector import connect
    except ImportError:
        from cator.common import connect


class MysqlDatabaseProxy(DatabaseProxy):
    """
    doc:
    mysql-connector-python: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    pymysql: https://pymysql.readthedocs.io/
    """

    def connect(self):
        self._connection = connect(**self.config)
        logger.debug("Database open")
