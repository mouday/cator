# -*- coding: utf-8 -*-
from cator.base.dbapi import ParamStyleEnum


class SqlUtil(object):
    """
    sql builder util
    """
    column_format = '`{}`'

    # don't support 'numeric'
    paramstyle_map = {
        'qmark': '?',
        'named': ':{}',
        'format': '%s',
        'pyformat': '%({})s'
    }

    @classmethod
    def backquote(cls, *args):
        """两侧增加反引号"""
        return ''.join(['`', *args, '`'])

    @classmethod
    def parentheses(cls, *args):
        """两侧增加括号"""
        return ' '.join(['(', *args, ')'])

    @classmethod
    def column_sql(cls, column):
        """
        获取 列名 的sql
        """
        return cls.column_format.format(column)

    @classmethod
    def columns_sql(cls, columns):
        """
        获取 列名 的字符串拼接
        """
        return ", ".join([cls.column_sql(column) for column in columns])

    @classmethod
    def placeholder_sql(cls, column, paramstyle=ParamStyleEnum.pyformat):
        """
        获取 占位符 的sql
        """
        if isinstance(paramstyle, ParamStyleEnum):
            paramstyle = paramstyle.value

        return cls.paramstyle_map[paramstyle].format(column)

    @classmethod
    def placeholders_sql(cls, columns, paramstyle=ParamStyleEnum.pyformat):
        """
        获取 占位符 的字符串拼接
        '%(name)s, %(age)s'
        """
        return ", ".join([
            cls.placeholder_sql(column=column, paramstyle=paramstyle)
            for column in columns
        ])

    @classmethod
    def column_operation_sql(cls, column, operator='=', paramstyle=ParamStyleEnum.pyformat):
        """
        获取 列名-占位符 的字符串拼接
        """
        return " ".join(
            [
                cls.column_sql(column),
                operator,
                cls.placeholder_sql(column=column, paramstyle=paramstyle)
            ])

    @classmethod
    def columns_operation_sql(cls, columns, operator='=', paramstyle=ParamStyleEnum.pyformat):
        """
        获取 列名-占位符 的字符串拼接
        """
        return ", ".join([
            cls.column_operation_sql(column=column, operator=operator, paramstyle=paramstyle)
            for column in columns
        ])

    @classmethod
    def get_list_columns(cls, lst):
        """
        :param lst: list[dict]
        :return:
        """
        columns = set()
        for row in lst:
            columns.update(row.keys())

        return list(columns)
