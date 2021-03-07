# -*- coding: utf-8 -*-
import sqlite3

from ..base import Database
from ..sql import SqlUtil
from .table import SqliteTable


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
    doc: https://docs.python.org/zh-cn/3.7/library/sqlite3.html
    """

    def __init__(self, autocommit=False, **kwargs):
        super().__init__(**kwargs)
        self.autocommit = autocommit

    def cursor(self, *args, **kwargs):
        if self.connection is None:
            self.connect()

        return self.connection.cursor()

    def connect(self):
        self.connection = sqlite3.connect(**self.config)
        self.connection.row_factory = dict_factory

    def before_execute(self, sql, params=None):
        _sql = SqlUtil.prepare_sqlite_sql(sql)
        return super().before_execute(_sql, params)

    def after_execute(self, cursor):
        """自动提交"""
        if self.autocommit:
            self.connection.commit()
        return cursor

    @property
    def tables(self):
        sql = 'SELECT `name` FROM SQLITE_MASTER WHERE type="table"'
        rows = self.select(sql=sql)
        return [row['name'] for row in rows]

    def table(self, table_name):
        return SqliteTable(database=self, table_name=table_name)
