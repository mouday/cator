# -*- coding: utf-8 -*-
"""
Python Database API Specification v2.0
https://www.python.org/dev/peps/pep-0249/
"""
import re

from abc import ABC
from enum import Enum


class ParamStyleEnum(Enum):
    """paramstyle"""
    qmark = 'qmark'  # ?
    numeric = 'numeric'  # :1
    named = 'named'  # :name
    format = 'format'  # %s
    pyformat = 'pyformat'  # %(name)s


class ApiLevelEnum(Enum):
    """apilevel"""
    one = '1.0'
    two = '2.0'


class ThreadSafetyEnum(Enum):
    """threadsafety"""
    not_share = 0
    share_not_connections = 1
    share_connections = 2
    share_connections_cursors = 3


class Connection(ABC):
    def close(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        pass


class ConnectionExtension(ABC):
    @property
    def messages(self):
        pass


class Cursor(ABC):
    @property
    def description(self):
        """read-only"""
        pass

    @property
    def rowcount(self):
        """read-only"""
        pass

    @property
    def arraysize(self):
        """read/write attribute"""
        pass

    @arraysize.setter
    def arraysize(self, size=None):
        """read/write attribute"""
        pass

    def callproc(self, procname, parameters=None):
        pass

    def close(self):
        pass

    def execute(self, operation, parameters=None):
        pass

    def executemany(self, operation, seq_of_parameters):
        pass

    def fetchone(self):
        pass

    def fetchmany(self, size=None):
        pass

    def fetchall(self):
        pass

    def nextset(self):
        pass

    def setinputsizes(self, sizes):
        pass

    def setoutputsize(self, size, column):
        pass


class CursorExtension(ABC):
    @property
    def rownumber(self):
        """read-only"""
        pass

    @property
    def connection(self):
        """read-only"""
        pass

    @property
    def lastrowid(self):
        """read-only"""
        pass

    def scroll(self, value, mode='relative'):
        pass

    @property
    def messages(self):
        pass

    def next(self):
        pass

    def __iter__(self):
        pass


def connect(*arg, **kwargs) -> Connection:
    """Constructors"""
    pass


################################
# ParamStyle Convert
################################

class ParamStyleConvert(object):
    @classmethod
    def named_to_pyformat(cls, sql):
        """
        :name -> %(name)s
        """
        return re.sub(r":(?P<key>\w+)", r"%(\g<key>)s", sql)

    @classmethod
    def pyformat_to_named(cls, sql):
        """
        %(name)s -> :name
        """
        return re.sub(r"%\((?P<key>\w+)\)s", r":\g<key>", sql)

    @classmethod
    def qmark_to_format(cls, sql):
        """
        ? -> %s
        """
        return sql.replace("?", "%s")

    @classmethod
    def format_to_qmark(cls, sql):
        """
        %s -> ?
        """
        return sql.replace("%s", "?")

    @classmethod
    def named_qmark_to_format_pyformat(cls, sql):
        """
        :name -> %(name)s
        ? -> %s
        required eg: pymysql
        """
        sql = cls.named_to_pyformat(sql)
        sql = cls.qmark_to_format(sql)
        return sql

    @classmethod
    def format_pyformat_to_named_qmark(cls, sql):
        """
        %(name)s -> :name
        %s -> ?
        required eg: sqlite
        """
        sql = cls.pyformat_to_named(sql)
        sql = cls.format_to_qmark(sql)
        return sql

    @classmethod
    def convert(cls, paramstyle, sql):
        convert_map = {
            ParamStyleEnum.qmark.value: cls.format_pyformat_to_named_qmark,
            ParamStyleEnum.pyformat.value: cls.named_qmark_to_format_pyformat,
        }

        return convert_map[paramstyle](sql)
