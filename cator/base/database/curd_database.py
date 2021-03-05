# -*- coding: utf-8 -*-
from typing import Union, List, Dict

from cator.base.database.cursor import Cursor


class CurdDatabase(Cursor):
    """
    以下是快捷操作
    """

    def select(self, operation, params=()) -> List:
        cursor = self.execute(operation=operation, params=params)
        return cursor.fetchall()

    def select_one(self, operation, params=()) -> Dict:
        cursor = self.execute(operation=operation, params=params)
        return cursor.fetchone()

    def update(self, operation, params=()) -> int:
        cursor = self.execute(operation=operation, params=params)
        return cursor.rowcount

    def delete(self, operation, params=()) -> int:
        cursor = self.execute(operation=operation, params=params)
        return cursor.rowcount

    def insert(self, operation, params: Union[list, dict]) -> int:
        cursor = self.execute(operation=operation, params=params)
        return cursor.rowcount

    def insert_one(self, operation, params: Union[tuple, dict] = ()) -> int:
        cursor = self.execute(operation=operation, params=params)
        return cursor.lastrowid
