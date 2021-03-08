# -*- coding: utf-8 -*-
from .db_url import parse_url_to_dict
from .base import DatabaseProxy
from .mysql import MysqlDatabaseProxy
from .sqlite import SqliteDatabaseProxy

schemes = {
    'mysql': MysqlDatabaseProxy,
    'sqlite': SqliteDatabaseProxy,
}


def connect(db_url) -> DatabaseProxy:
    config = parse_url_to_dict(db_url=db_url)
    scheme = config.pop('scheme')

    return schemes[scheme](**config)


Connect = connect
