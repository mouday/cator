# -*- coding: utf-8 -*-
from mysql.connector import Connect
from cator.logger import logger
from ..base import Database
from ..sql import SqlUtil
from .table import MysqlTable


class MysqlDatabase(Database):
    """
    doc: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    """

    def cursor(self):
        return self.connection.cursor(dictionary=True)

    def start_transaction(self):
        return self._connection.start_transaction()

    @property
    def autocommit(self):
        return self._connection.autocommit

    @autocommit.setter
    def autocommit(self, value: bool):
        self._connection.autocommit = value

    def connect(self):
        self._connection = Connect(**self.config)
        logger.debug("Database open")

    def start_transaction(self, consistent_snapshot=False,
                          isolation_level=None, readonly=None):
        self._connection.start_transaction(
            consistent_snapshot=consistent_snapshot,
            isolation_level=isolation_level,
            readonly=readonly)

    def before_execute(self, sql, params=None):
        sql = SqlUtil.prepare_mysql_sql(sql)
        return super().before_execute(sql, params)

    @property
    def tables(self):
        # sql = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = :database'
        # sql = 'show tables'
        sql = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE()'
        # params = {'database': self.config['database']}
        rows = self.select(sql=sql)
        return [row['TABLE_NAME'] for row in rows]

    def table(self, table_name):
        return MysqlTable(database=self, table_name=table_name)
