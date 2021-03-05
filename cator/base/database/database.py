# -*- coding: utf-8 -*-

from cator.base.database.curd_database import CurdDatabase


class Database(CurdDatabase):
    @property
    def tables(self):
        raise NotImplementedError

    def table(self, table_name):
        raise NotImplementedError
