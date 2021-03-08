# -*- coding: utf-8 -*-
from .base import DatabaseProxy
from .db_url import parse_url_to_dict
from .mysql import MysqlDatabaseProxy
from .sqlite import SqliteDatabaseProxy

schemes = {
    'mysql': MysqlDatabaseProxy,
    'sqlite': SqliteDatabaseProxy,
}


def connect(db_uri) -> DatabaseProxy:
    config = parse_url_to_dict(db_uri=db_uri)
    scheme = config.pop('scheme')

    return schemes[scheme](**config)


Connect = connect
