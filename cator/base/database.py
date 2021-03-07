# -*- coding: utf-8 -*-
from typing import List, Union, Dict

from cator.logger import logger
from .table import Table


class Database(object):
    def __init__(self, **kwargs):
        self.connection = None
        self.config = kwargs

    @property
    def tables(self) -> List:
        """获取数据库中的表名"""
        raise NotImplementedError

    def table(self, table_name) -> Table:
        """获取表操作对象"""
        raise NotImplementedError

    def cursor(self, *args, **kwargs):
        """返回cursor 对象"""
        raise NotImplementedError()

    def connect(self):
        """连接数据库"""
        raise NotImplementedError()

    def close(self):
        """关闭游标和连接"""
        if hasattr(self.connection, 'close'):
            self.connection.close()

        logger.debug("Database close")

    def before_execute(self, sql: str, params=None):
        """执行前"""
        logger.debug('%s %s', sql, params)
        return sql

    def after_execute(self, cursor):
        """执行后"""
        return cursor

    def execute(self, sql: str, params=None):
        """
        执行sql 语句
        :param sql:
        :param params: dict/tuple、list[dict]/list[tuple]
        :return:
        """

        _sql = self.before_execute(sql=sql, params=params)

        cursor = self.cursor()

        # mysql 和 sqlite3 关键字参数不一样,只能使用位置参数
        if isinstance(params, list):
            cursor.executemany(_sql, params)
        elif params:
            cursor.execute(_sql, params)
        else:
            cursor.execute(_sql)

        return self.after_execute(cursor)

    def select(self, sql: str, params=()) -> List:
        """查询多行数据"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.fetchall()

    def select_one(self, sql: str, params=()) -> Dict:
        """查询一行数据"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.fetchone()

    def update(self, sql: str, params=()) -> int:
        """更新数据"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def delete(self, sql: str, params=()) -> int:
        """删除数据"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def insert(self, sql: str, params: Union[list, dict]) -> int:
        """插入一行或多行数据"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def insert_one(self, sql: str, params: Union[tuple, dict] = ()) -> int:
        """插入一行数据"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.lastrowid