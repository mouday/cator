# -*- coding: utf-8 -*-
from .dict_mysql_database import DictMySQLDatabase


def register_dict_database(name='mysql+dict'):
    from playhouse.db_url import register_database
    register_database(DictMySQLDatabase, name)
