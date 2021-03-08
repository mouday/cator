# -*- coding: utf-8 -*-
from enum import Enum
from sqlite3 import connect, paramstyle

from cator.base.dbapi import ParamStyleConvert
from cator.logger import logger

from .table import SqliteTable
from ..base import Database


# doc： https://www.sqlite.org/lang_transaction.html#immediate
class IsolationLevel(Enum):
    DEFERRED = 'DEFERRED'  # default
    IMMEDIATE = 'IMMEDIATE'
    EXCLUSIVE = 'EXCLUSIVE'


class SqliteDatabase(Database):
    """
    autocommit: 指定参数 isolation_level=null
    doc: https://docs.python.org/zh-cn/3.7/library/sqlite3.html
    """

    def connect(self):
        self._connection = connect(**self.config)
        logger.debug("Database open")

    def before_execute(self, sql, params=None):
        sql = ParamStyleConvert.convert(paramstyle=paramstyle, sql=sql)
        return super().before_execute(sql, params)

    @property
    def tables(self):
        sql = 'SELECT `name` FROM SQLITE_MASTER WHERE type="table"'
        rows = self.select(sql=sql)
        return [row['name'] for row in rows]

    def table(self, table_name):
        return SqliteTable(database=self, table_name=table_name)
