# -*- coding: utf-8 -*-
import re


class SqlUtil(object):
    """
    """
    column_format = '`{}`'

    placeholder_format = '%({})s'

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
    def placeholder_sql(cls, column):
        """
        获取 占位符 的sql
        """
        return cls.placeholder_format.format(column)

    @classmethod
    def placeholders_sql(cls, columns):
        """
        获取 占位符 的字符串拼接
        '%(name)s, %(age)s'
        """
        return ", ".join([cls.placeholder_sql(column) for column in columns])

    @classmethod
    def column_operation_sql(cls, column, operator='='):
        """
        获取 列名-占位符 的字符串拼接
        """
        return " ".join(
            [
                cls.column_sql(column),
                operator,
                cls.placeholder_sql(column)
            ])

    @classmethod
    def columns_operation_sql(cls, columns, operator='='):
        """
        获取 列名-占位符 的字符串拼接
        """
        return ", ".join([cls.column_operation_sql(column, operator) for column in columns])

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

    @classmethod
    def column_in(cls, column, list_params):
        data = {}
        for index, value in enumerate(list_params):
            data[f'{column}-{index}'] = value

        return cls.parentheses(cls.placeholders_sql(data.keys())), data

    @classmethod
    def compile_mysql_sql(cls, sql):
        """转换sql中变量占位符 :key -> %(key)s"""
        return re.sub(r":(?P<key>\w+)", r"%(\g<key>)s", sql)

    @classmethod
    def replace_mysql_sql(cls, sql):
        """占位符替换 ? -> %s """
        return sql.replace("?", "%s")

    @classmethod
    def prepare_mysql_sql(cls, sql):
        """
        占位符再进行预处理, 支持4种占位符：
            :key -> %(key)s
            ? -> %s
        :param sql: sql
        :return:
        """
        sql = cls.compile_mysql_sql(sql=sql)
        sql = cls.replace_mysql_sql(sql=sql)

        return sql

    @classmethod
    def compile_sqlite_sql(cls, sql):
        """转换sql中变量占位符 %(key)s -> :key"""
        return re.sub(r"%\((?P<key>\w+)\)s", r":\g<key>", sql)

    @classmethod
    def replace_sqlite_sql(cls, sql):
        """占位符替换 ? -> %s """
        return sql.replace("%s", "?")

    @classmethod
    def prepare_sqlite_sql(cls, sql):
        """
        占位符再进行预处理, 支持4种占位符：
            %(key)s  ->  :key
            %s -> ?
        :param sql: sql
        :return:
        """
        sql = cls.compile_sqlite_sql(sql=sql)
        sql = cls.replace_sqlite_sql(sql=sql)

        return sql
