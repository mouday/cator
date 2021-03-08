# -*- coding: utf-8 -*-

# peewee use pymysql
from cator.base import DatabaseProxy

try:
    # pymysql
    from pymysql import connect, paramstyle
except ImportError:
    # mysql-connector-python
    from mysql.connector import connect, paramstyle


from cator.logger import logger


class MysqlDatabaseProxy(DatabaseProxy):
    """
    doc:
    mysql-connector-python: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    pymysql: https://pymysql.readthedocs.io/
    """

    def connect(self):
        self._connection = connect(**self.config)
        logger.debug("Database open")
