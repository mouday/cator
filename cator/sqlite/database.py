# -*- coding: utf-8 -*-
from enum import Enum

try:
    from sqlite3 import connect
except ImportError:
    from cator.common import connect

from cator.base.database import DatabaseProxy
from cator.logger import logger


# doc： https://www.sqlite.org/lang_transaction.html#immediate
class IsolationLevelEnum(Enum):
    DEFERRED = 'DEFERRED'  # default
    IMMEDIATE = 'IMMEDIATE'
    EXCLUSIVE = 'EXCLUSIVE'


class SqliteDatabaseProxy(DatabaseProxy):
    """
    autocommit: 指定参数 isolation_level=null
    doc: https://docs.python.org/zh-cn/3.7/library/sqlite3.html
    """

    def __init__(self, connection=None, paramstyle='qmark', **kwargs):
        super().__init__(connection, paramstyle, **kwargs)

    def connect(self):
        logger.debug("Database open")
        return connect(**self.config)
