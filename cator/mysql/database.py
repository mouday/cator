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

    def cursor(self, buffered=None, raw=None,
               prepared=None, cursor_class=None,
               dictionary=True, named_tuple=None):
        if self.connection is None:
            self.connect()

        return self.connection.cursor(
            buffered=buffered, raw=raw,
            prepared=prepared, cursor_class=cursor_class,
            dictionary=dictionary, named_tuple=named_tuple)

    def connect(self):
        self.connection = Connect(**self.config)
        logger.debug("Database open")

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
