# -*- coding: utf-8 -*-
from .db_url import parse_url_to_dict
from .base.database import DatabaseProxy
from .mysql.database import MysqlDatabaseProxy, MysqlReconnectDatabaseProxy
from .sqlite.database import SqliteDatabaseProxy

schemes = {
    'mysql': MysqlDatabaseProxy,
    'mysql+reconnect': MysqlReconnectDatabaseProxy,
    'sqlite': SqliteDatabaseProxy,
}


def connect(db_uri=None, **kwargs) -> DatabaseProxy:
    if db_uri:
        config = parse_url_to_dict(db_uri=db_uri)
    else:
        config = kwargs

    scheme = config.pop('scheme')

    return schemes[scheme](**config)


Connect = connect
