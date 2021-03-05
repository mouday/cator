# -*- coding: utf-8 -*-
from mysql.connector import Connect

from cator.base import Database
from cator.sql import SqlUtil
from .table import MysqlTable


class MysqlDatabase(Database):
    """
    doc: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection = Connect(**kwargs)
        self.cursor = self.connection.cursor(dictionary=True)

    def before_execute(self, operation, params=None):
        sql = SqlUtil.prepare_mysql_sql(operation)
        return super().before_execute(sql, params)

    @property
    def tables(self):
        # sql = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = :database'
        # sql = 'show tables'
        sql = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE()'
        # params = {'database': self.config['database']}
        rows = self.select(operation=sql)
        print(rows)
        return [row['TABLE_NAME'] for row in rows]

    def table(self, table_name):
        return MysqlTable(database=self, table_name=table_name)
