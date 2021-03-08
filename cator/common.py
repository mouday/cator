# -*- coding: utf-8 -*-


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
