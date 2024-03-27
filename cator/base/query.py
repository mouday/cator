# -*- coding: utf-8 -*-
"""
@File    : query.py
@Date    : 2024-03-27
"""
from __future__ import annotations

from collections import OrderedDict

from .dbapi import ParamStyleEnum
from ..sql import SqlBuilder, SqlUtil

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .table import Table
    from .database import DatabaseProxy


class Query(object):
    def __init__(self, database: DatabaseProxy, table: Table = None):
        self.database = database
        self.table = table
        self.sql_build = SqlBuilder()
        self.params = []

    def from_(self, table: Table):
        self.table = table
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
        values = OrderedDict(sorted(data.items()))

        sql = (SqlBuilder()
               .update(self.table.backquote_table_name)
               .set(values.keys(), paramstyle=ParamStyleEnum.qmark)
               .extend(self.sql_build.build())
               .build()
               )

        bindings = tuple(list(values.values()) + self.params)

        return self.database.update(sql=sql, params=bindings)

    def delete(self):
        sql = (SqlBuilder()
               .delete_from(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build())

        return self.database.delete(sql=sql, params=tuple(self.params))

    def select(self, columns='*'):
        if isinstance(columns, list):
            columns = SqlUtil.columns_sql(columns)

        sql = (SqlBuilder()
               .select(columns)
               .from_(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build()
               )

        return self.database.select(sql=sql, params=tuple(self.params))

    def first(self, columns='*'):
        if isinstance(columns, list):
            columns = SqlUtil.columns_sql(columns)

        self.sql_build.limit(1)

        sql = (SqlBuilder()
               .select(columns)
               .from_(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build()
               )

        return self.database.select_one(sql=sql, params=tuple(self.params))

    def count(self, alias='total'):
        sql = (SqlBuilder()
               .select('count(*) as ' + alias)
               .from_(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build()
               )

        row = self.database.select_one(sql=sql, params=tuple(self.params))
        return row[alias]
