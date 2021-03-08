# -*- coding: utf-8 -*-

# peewee use pymysql
try:
    # pymysql
    from pymysql import connect, paramstyle
except ImportError:
    # mysql-connector-python
    from mysql.connector import connect, paramstyle

from cator.base import Database
from cator.base.dbapi import ParamStyleConvert
from cator.logger import logger

from .table import MysqlTable


class MysqlDatabase(Database):
    """
    doc:
    mysql-connector-python: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    pymysql: https://pymysql.readthedocs.io/
    """

    def connect(self):
        self._connection = connect(**self.config)
        logger.debug("Database open")

    def before_execute(self, sql, params=None):
        sql = ParamStyleConvert.convert(paramstyle=paramstyle, sql=sql)
        return super().before_execute(sql=sql, params=params)

    @property
    def tables(self):
        sql = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE()'
        rows = self.select(sql=sql)
        return [row['TABLE_NAME'] for row in rows]

    def table(self, table_name):
        return MysqlTable(database=self, table_name=table_name)
