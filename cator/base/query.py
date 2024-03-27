# -*- coding: utf-8 -*-
"""
@File    : query.py
@Date    : 2024-03-27
"""
from __future__ import annotations

from ..sql import SqlBuilder

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .table import Table
    from .database import DatabaseProxy


class Query(object):
    def __init__(self, database: DatabaseProxy, table: Table = None):
        self.database = database
        self.table = table
        self.sql_build = SqlBuilder()

    def from_(self, table: Table):
        self.table = table
        return self

    def where(self, sql: str):
        self.sql_build.where(sql)
        return self

    def order_by(self, sql: str):
        self.sql_build.order_by(sql)
        return self

    def limit(self, sql: str):
        self.sql_build.limit(sql)
        return self

    def offset(self, sql: str):
        self.sql_build.offset(sql)
        return self

    def group_by(self, sql: str):
        self.sql_build.group_by(sql)
        return self

    def having(self, sql: str):
        self.sql_build.having(sql)
        return self

    def join(self, sql: str):
        self.sql_build.join(sql)
        return self

    def update(self, data: dict):
        sql = (SqlBuilder()
               .update(self.table.backquote_table_name)
               .set(data.keys())
               .extend(self.sql_build.build())
               .build()
               )

        return self.database.update(sql, data)

    def delete(self):
        sql = (SqlBuilder()
               .delete_from(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build())

        return self.database.delete(sql)

    def select(self, columns='*'):
        sql = (SqlBuilder()
               .select(columns)
               .from_(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build()
               )

        return self.database.select(sql)

    def first(self, columns='*'):
        self.sql_build.limit(1)

        sql = (SqlBuilder()
               .select(columns)
               .from_(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build()
               )

        return self.database.select_one(sql)

    def count(self):
        sql = (SqlBuilder()
               .select('count(*) as total')
               .from_(self.table.backquote_table_name)
               .extend(self.sql_build.build())
               .build()
               )

        row = self.database.select_one(sql=sql)
        return row['total']
