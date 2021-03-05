# -*- coding: utf-8 -*-
from cator.base.table.curd_table import CurdTable


class Table(CurdTable):

    @property
    def columns(self):
        raise NotImplementedError

