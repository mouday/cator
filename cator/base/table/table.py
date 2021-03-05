# -*- coding: utf-8 -*-
from typing import List

from cator.base.table.curd_table import CurdTable


class Table(CurdTable):

    @property
    def columns(self) -> List:
        raise NotImplementedError
