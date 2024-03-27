# -*- coding: utf-8 -*-
"""
@File    : reconnect_mixin.py
@Date    : 2024-03-27
"""
from cator import DatabaseProxy
from cator.logger import logger


class ReconnectMixin(DatabaseProxy):
    """
    code ref: peewee playhouse/shortcuts.py
    """

    def is_reconnect_error(self, error):
        """
        need implement this function, tell me need reconnect database.
        :param error:
        :return: bool
        """
        return False

    def execute(self, sql, params=None):
        try:
            return super(ReconnectMixin, self).execute(sql, params)
        except Exception as error:
            if not self.is_reconnect_error(error):
                raise error

            logger.debug('reconnect database reason: %s', error)

            if self.is_connected():
                self.close()

            return super(ReconnectMixin, self).execute(sql, params)
