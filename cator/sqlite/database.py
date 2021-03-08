# -*- coding: utf-8 -*-
import sqlite3

from ..base import Database
from ..sql import SqlUtil
from .table import SqliteTable
from enum import Enum


# doc： https://www.sqlite.org/lang_transaction.html#immediate
class IsolationLevel(Enum):
    DEFERRED = 'DEFERRED'  # default
    IMMEDIATE = 'IMMEDIATE'
    EXCLUSIVE = 'EXCLUSIVE'


def dict_factory(cursor, row):
    """
    查询结果转为dict
    see: https://docs.python.org/zh-cn/3.7/library/sqlite3.html#sqlite3.Connection.row_factory
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteDatabase(Database):
    """
    autocommit: 指定参数 isolation_level=null
    doc: https://docs.python.org/zh-cn/3.7/library/sqlite3.html
    """

    def cursor(self):
        return self.connection.cursor()

    @property
    def isolation_level(self):
        return self._connection.isolation_level

    @isolation_level.setter
    def isolation_level(self, value: bool):
        self._connection.isolation_level = value

    def connect(self):
        self._connection = sqlite3.connect(**self.config)
        self._connection.row_factory = dict_factory

    def before_execute(self, sql, params=None):
        _sql = SqlUtil.prepare_sqlite_sql(sql)
        return super().before_execute(_sql, params)

    @property
    def tables(self):
        sql = 'SELECT `name` FROM SQLITE_MASTER WHERE type="table"'
        rows = self.select(sql=sql)
        return [row['name'] for row in rows]

    def table(self, table_name):
        return SqliteTable(database=self, table_name=table_name)
