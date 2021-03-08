# -*- coding: utf-8 -*-
from .base import Database
from .db_url import parse_url_to_dict
from .mysql import MysqlDatabase
from .sqlite import SqliteDatabase


schemes = {
    'mysql': MysqlDatabase,
    'sqlite': SqliteDatabase,
}


def connect(db_url) -> Database:
    config = parse_url_to_dict(db_url=db_url)
    scheme = config.pop('scheme')

    return schemes[scheme](**config)


Connect = connect
