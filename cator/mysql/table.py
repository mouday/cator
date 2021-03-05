# -*- coding: utf-8 -*-
from cator.base import Table


class MysqlTable(Table):

    @property
    def columns(self):
        sql = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = :table_name'
        params = {'table_name': self.table_name}
        rows = self.database.select(operation=sql, params=params)
        return [row['COLUMN_NAME'] for row in rows]
