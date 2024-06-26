# -*- coding: utf-8 -*-
from functools import partial

from cator.base.dbapi import ParamStyleEnum
from .sql_util import SqlUtil


class SqlBuilder(object):
    """
    适用于简单sql构造
    eg: insert update delete
    """

    def __init__(self):
        self._sql = []

    def __getattr__(self, key):
        return partial(self.append, key)

    def append(self, key, *args):
        self._sql.append(self.upper_keywords(key))
        self._sql.extend(args)
        return self

    def extend(self, *args):
        self._sql.extend(args)
        return self

    def set(self, columns, *args, paramstyle=ParamStyleEnum.pyformat):
        sql = SqlUtil.columns_operation_sql(columns=columns, operator='=', paramstyle=paramstyle)
        self.append('set', sql, *args)
        return self

    def values(self, columns, *args, paramstyle=ParamStyleEnum.pyformat):
        pre_sql = SqlUtil.parentheses(SqlUtil.columns_sql(columns))
        after_sql = SqlUtil.parentheses(SqlUtil.placeholders_sql(columns=columns, paramstyle=paramstyle))
        self._sql.append(pre_sql)
        self.append('values', after_sql, *args)
        return self

    def build(self):
        return " ".join([str(sql) for sql in self._sql])

    @classmethod
    def upper_keywords(cls, keywords):
        """关键词大写"""
        return keywords.upper().strip("_").replace("_", " ")

    def __str__(self):
        return self.build()
