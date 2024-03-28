# -*- coding: utf-8 -*-
"""
@File    : query.py
@Date    : 2024-03-27
"""
from __future__ import annotations

from collections import OrderedDict

from .collection import Collection
from .dbapi import ParamStyleEnum
from ..sql import SqlBuilder, SqlUtil

from typing import TYPE_CHECKING, Union, List, Dict

if TYPE_CHECKING:
    from .database import DatabaseProxy


class Query(object):
    def __init__(self, database: DatabaseProxy):
        self.database = database
        self.table = None
        self._table = None
        self.sql_build = SqlBuilder()
        self.params = []

    def from_(self, table: str):
        self.table = table
        self._table = SqlUtil.backquote(self.table)
        return self

    def where(self, sql: str, *args):
        self.sql_build.where(sql)
        self.params.extend(args)
        return self

    def order_by(self, sql: str, *args):
        self.sql_build.order_by(sql)
        self.params.extend(args)
        return self

    def limit(self, arg):
        self.sql_build.limit('?')
        self.params.append(arg)
        return self

    def offset(self, arg: str):
        self.sql_build.offset('?')
        self.params.append(arg)
        return self

    def group_by(self, sql: str, *args):
        self.sql_build.group_by(sql)
        self.params.extend(args)
        return self

    def having(self, sql: str, *args):
        self.sql_build.having(sql)
        self.params.extend(args)
        return self

    def join(self, sql: str, *args):
        self.sql_build.join(sql)
        self.params.extend(args)
        return self

    def update(self, data: dict):
        """
        update rows and return row count
        :param data:
        :return: row_count
        """
        if not data:
            return 0

        values = OrderedDict(sorted(data.items()))

        sql = (SqlBuilder()
               .update(self._table)
               .set(values.keys(), paramstyle=ParamStyleEnum.qmark)
               .extend(self.sql_build.build())
               .build()
               )

        bindings = tuple(list(values.values()) + self.params)

        return self.database.update(sql=sql, params=bindings)

    def delete(self) -> int:
        """
        execute delete rows and return row count
        :return: row_count
        """
        sql = (SqlBuilder()
               .delete_from(self._table)
               .extend(self.sql_build.build())
               .build())

        return self.database.delete(sql=sql, params=tuple(self.params))

    def select(self, columns: Union[str, List, None] = None) -> List[Dict]:
        """
        select rows
        :param columns:
        :return:
        """
        if columns is None:
            columns = '*'
        elif isinstance(columns, list):
            columns = SqlUtil.columns_sql(columns)

        sql = (SqlBuilder()
               .select(columns)
               .from_(self._table)
               .extend(self.sql_build.build())
               .build()
               )

        return self.database.select(sql=sql, params=tuple(self.params))

    def select_one(self, columns: Union[str, List, None] = None) \
            -> Union[Dict, None]:

        if 'LIMIT' not in self.sql_build.build():
            self.sql_build.limit(1)

        rows = self.select(columns)

        return Collection(rows).first()

    def select_page(self, page: int, size: int, columns=None):
        self.sql_build.limit('?').offset('?')
        self.params.extend([size, (page - 1) * size])
        return self.select(columns)

    def select_count(self, column: str = None) -> int:
        """
        获取统计总数
        :param column: str 别名
        :return:
        """
        if column:
            column = f'count(`{column}`)'
        else:
            column = 'count(*)'

        rows = self.select(column)

        return Collection(rows).first()[column]

    def increment(self, column, amount=1):
        """

        :param column:
        :param amount:
        :return: row_count
        """
        sql = (SqlBuilder()
               .update(self._table)
               .append('set', f'`{column}` = `{column}` + ?')
               .extend(self.sql_build.build())
               .build()
               )

        bindings = tuple([amount] + self.params)

        return self.database.update(sql=sql, params=bindings)

    def decrement(self, column, amount=1):
        sql = (SqlBuilder()
               .update(self._table)
               .append('set', f'`{column}` = `{column}` - ?')
               .extend(self.sql_build.build())
               .build()
               )

        bindings = tuple([amount] + self.params)

        return self.database.update(sql=sql, params=bindings)
