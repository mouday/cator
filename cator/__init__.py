# -*- coding: utf-8 -*-
from cator.base.database.database import Database
from cator.db_url import parse_url_to_dict
from cator.mysql.database import MysqlDatabase
from cator.sqlite.database import SqliteDatabase

schemes = {
    'mysql': MysqlDatabase,
    'sqlite': SqliteDatabase
}


def connect(db_url) -> Database:
    config = parse_url_to_dict(db_url=db_url)
    scheme = config.pop('scheme')

    return schemes[scheme](**config)


Connect = connect
