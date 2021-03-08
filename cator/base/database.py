# -*- coding: utf-8 -*-
from typing import List, Union, Dict

from cator.base.dbapi import Connection
from cator.common import dict_factory
from cator.logger import logger
from .table import Table


class Database(Connection):
    def __init__(self, connection: Connection = None, **kwargs):
        self._connection = connection
        self.config = kwargs

    ############################################
    # connection
    ############################################
    @property
    def connection(self):
        if self._connection is None:
            self.connect()

        return self._connection

    def connect(self):
        """连接数据库"""
        raise NotImplementedError()

    ############################################
    # DB API V2.0
    ############################################
    def cursor(self):
        """返回cursor 对象"""
        return self.connection.cursor()

    def close(self):
        """关闭连接"""
        if hasattr(self._connection, 'close'):
            self._connection.close()

        self._connection = None
        logger.debug("Database close")

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    ############################################
    # table
    ############################################

    @property
    def tables(self) -> List:
        """获取数据库中的表名"""
        raise NotImplementedError

    def table(self, table_name) -> Table:
        """获取表操作对象"""
        raise NotImplementedError

    ############################################
    # execute
    ############################################

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
        :param params:
                 params type        | call method
            -----------------------------------------
            dict/tuple/None         | execute
            list[dict]/list[tuple]  | executemany
            -----------------------------------------
        :return:
        """

        sql = self.before_execute(sql=sql, params=params)

        cursor = self.cursor()

        # mysql 和 sqlite3 关键字参数不一样,只能使用位置参数
        if isinstance(params, list):
            cursor.executemany(sql, params)
        elif params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        return self.after_execute(cursor)

    ############################################
    # curd
    ############################################

    def select(self, sql: str, params=None) -> List:
        """select rows and return rows as list"""
        cursor = self.execute(sql=sql, params=params)
        return [dict_factory(cursor, row) for row in cursor.fetchall()]

    def select_one(self, sql: str, params=None) -> Dict:
        """select rows and return one row as dict"""
        cursor = self.execute(sql=sql, params=params)
        return dict_factory(cursor, cursor.fetchone())

    def update(self, sql: str, params=None) -> int:
        """update rows and return rowcount"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def delete(self, sql: str, params=None) -> int:
        """delete rows and return rowcount"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def insert(self, sql: str, params: Union[list, dict] = None) -> int:
        """insert one or many row and return rowcount"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def insert_one(self, sql: str, params: Union[tuple, dict] = None) -> int:
        """insert one row and return lastrowid"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.lastrowid
