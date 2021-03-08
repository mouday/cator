# -*- coding: utf-8 -*-
from typing import List, Dict, Union

from cator.common import dict_factory
from cator.mysql import MysqlTable

from cator.base.dbapi import ParamStyleConvert

# peewee is optional
try:
    from peewee import MySQLDatabase
except ImportError:
    MySQLDatabase = object


class DictMySQLDatabase(MySQLDatabase):
    """扩展peewee sql查询方法，返回值处理为dict"""

    def before_query(self, sql):
        """support named param style"""
        sql = ParamStyleConvert.convert('pyformat', sql)
        return sql

    def query(self, sql, params=None):
        """execute 方法被MySQLDatabase 使用了（^-^）"""
        sql = self.before_query(sql)

        cursor = self.cursor()

        # mysql 和 sqlite3 关键字参数不一样,只能使用位置参数
        if isinstance(params, list):
            cursor.executemany(sql, params)
        elif params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        return cursor

    def select(self, sql: str, params=None) -> List:
        """select many row"""
        cursor = self.query(sql=sql, params=params)
        return [dict_factory(cursor, row) for row in cursor.fetchall()]

    def select_one(self, sql: str, params=None) -> Dict:
        """select one row"""
        cursor = self.query(sql=sql, params=params)
        return dict_factory(cursor, cursor.fetchone())

    def update(self, sql: str, params=None) -> int:
        """update many row"""
        cursor = self.query(sql=sql, params=params)
        return cursor.rowcount

    def delete(self, sql: str, params=None) -> int:
        """delete many row"""
        cursor = self.query(sql=sql, params=params)
        return cursor.rowcount

    def insert(self, sql: str, params: Union[list, dict] = None) -> int:
        """insert many row"""
        cursor = self.query(sql=sql, params=params)
        return cursor.rowcount

    def insert_one(self, sql: str, params: Union[tuple, dict] = None) -> int:
        """insert one row"""
        cursor = self.query(sql=sql, params=params)
        return cursor.lastrowid

    def table(self, table_name: str) -> MysqlTable:
        """return a Table object"""
        return MysqlTable(self, table_name)
