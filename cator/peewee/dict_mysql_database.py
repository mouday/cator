# -*- coding: utf-8 -*-
from typing import List, Dict, Union

from cator.common import dict_factory
from cator.mysql import MysqlTable
from cator.sql import SqlUtil

try:
    from peewee import MySQLDatabase
except ImportError:
    MySQLDatabase = object


class DictMySQLDatabase(MySQLDatabase):
    """扩展peewee sql查询方法，返回值处理为dict"""

    def query(self, sql, params=None):
        """execute 方法被MySQLDatabase 使用了"""
        sql = SqlUtil.prepare_mysql_sql(sql)
        return self.execute_sql(sql, params)

    def select(self, sql: str, params=None) -> List:
        """select many row"""
        cursor = self.query(sql=sql, params=params)
        return [dict_factory(cursor, row) for row in cursor.fetchall()]

    def select_one(self, sql: str, params=None) -> Dict:
        """select one row"""
        cursor = self.query(sql=sql, params=params)
        row = cursor.fetchone()
        return dict_factory(cursor, row)

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

    def table(self, table_name):
        return MysqlTable(self, table_name)
