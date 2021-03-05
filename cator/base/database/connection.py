# -*- coding: utf-8 -*-

from cator.logger import logger


class Connection(object):
    def __init__(self, **kwargs):
        self.connection = None
        logger.debug("Database open")

    def close(self):
        """关闭游标和连接"""
        self.connection.close()
        logger.debug("Database close")
