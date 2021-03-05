# -*- coding: utf-8 -*-
from cator.base.database.connection import Connection
from cator.logger import logger


class Cursor(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = None

    def close(self):
        self.cursor.close()
        super().close()

    def before_execute(self, operation, params=None):
        logger.debug('[before_execute] %s %s', operation, params)
        return operation

    def after_execute(self, cursor):
        return cursor

    def execute(self, operation, params=None):
        """
        :param operation:
        :param params: dict/tuple、list[dict]/list[tuple]
        :return:
        """
        if self.cursor is None:
            raise Exception('cursor is None')

        operation = self.before_execute(operation=operation, params=params)

        # mysql 和 sqlite3 关键字参数不一样,只能使用位置参数
        if isinstance(params, list):
            self.cursor.executemany(operation, params)
        elif params:
            self.cursor.execute(operation, params)
        else:
            self.cursor.execute(operation)

        return self.after_execute(self.cursor)
