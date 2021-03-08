# -*- coding: utf-8 -*-
from typing import List, Union, Dict

from cator.base.connection import ConnectionProxy
from cator.base.dbapi import ParamStyleConvert, Connection
from cator.common import dict_factory
from cator.logger import logger
from .table import Table


class DatabaseProxy(ConnectionProxy):

    def __init__(self, connection: Connection = None, paramstyle='pyformat', **kwargs):
        super().__init__(connection, **kwargs)
        self.paramstyle = paramstyle

    ############################################
    # table
    ############################################
    def table(self, table_name) -> Table:
        """return Table object"""
        return Table(database=self, table_name=table_name)

    ############################################
    # execute
    ############################################

    def before_execute(self, sql: str, params=None):
        """before execute do something"""
        sql = ParamStyleConvert.convert(paramstyle=self.paramstyle, sql=sql)
        logger.debug('%s %s', sql, params)
        return sql

    def after_execute(self, cursor):
        """after execute do something"""
        return cursor

    def execute(self, sql: str, params=None):
        """
        execute sql with params
        :param sql:
        :param params:
                 params type        | call method
            -----------------------------------------
            dict/tuple/None         | execute
            list[dict]/list[tuple]  | executemany
            -----------------------------------------
        :return: cursor
        """

        sql = self.before_execute(sql=sql, params=params)

        cursor = self.cursor()

        # mysql and sqlite3 **kwargs is different, only use *args.
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
        """update rows and return row count"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def delete(self, sql: str, params=None) -> int:
        """delete rows and return row count"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def insert(self, sql: str, params: Union[list, dict] = None) -> int:
        """insert one or many row and return row count"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.rowcount

    def insert_one(self, sql: str, params: Union[tuple, dict] = None) -> int:
        """insert one row and return last row id"""
        cursor = self.execute(sql=sql, params=params)
        return cursor.lastrowid
