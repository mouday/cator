# -*- coding: utf-8 -*-
from typing import List
from cator.base import Table
from cator.base.database.curd_database import CurdDatabase


class Database(CurdDatabase):
    @property
    def tables(self) -> List:
        raise NotImplementedError

    def table(self, table_name) -> Table:
        raise NotImplementedError
