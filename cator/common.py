# -*- coding: utf-8 -*-
import time
from functools import wraps

from cator.logger import logger


def dict_factory(cursor, row):
    """
    convert cursor result to dict
    see: https://docs.python.org/zh-cn/3.7/library/sqlite3.html#sqlite3.Connection.row_factory
    """
    if not row:
        return

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect(*args, **kwargs):
    """default connect method"""
    raise Exception('database connect driver not install')


# 计时器
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time() * 1000
        ret = func(*args, **kwargs)
        end_time = time.time() * 1000
        logger.debug("time: %.2f ms" % (end_time - start_time))
        return ret

    return wrapper
