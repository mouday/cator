# -*- coding: utf-8 -*-
from cator.base import dbapi
from cator.logger import logger


class ConnectionProxy(dbapi.Connection):
    def __init__(self, connection=None, **kwargs):
        # type: (dbapi.Connection, any) -> None
        self._connection = connection
        self.config = kwargs

    ############################################
    # connection
    ############################################
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connect()

        return self._connection

    def is_connected(self):
        """
        @since v1.0.0
        :return:
        """
        return self._connection is not None

    def connect(self):
        # type: () -> dbapi.Connection
        """
        连接数据库
        """
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
