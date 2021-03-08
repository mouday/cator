# -*- coding: utf-8 -*-

from cator.base.dbapi import Connection
from cator.logger import logger


class ConnectionProxy(Connection):
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
    # DB API V2.0 implement
    ############################################
    def cursor(self):
        """return cursor object"""
        return self.connection.cursor()

    def close(self):
        """close connection"""
        if hasattr(self._connection, 'close'):
            self._connection.close()

        self._connection = None
        logger.debug("Database close")

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()
