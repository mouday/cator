# -*- coding: utf-8 -*-
from ..base import Table


class SqliteTable(Table):

    @property
    def columns(self):
        # sql = 'PRAGMA table_info([:table_name])'
        # equal
        sql = 'SELECT * FROM PRAGMA_TABLE_INFO(:table_name)'
        params = {'table_name': self.table_name}
        rows = self.database.select(sql=sql, params=params)
        return [row['name'] for row in rows]
