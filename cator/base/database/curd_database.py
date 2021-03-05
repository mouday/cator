# -*- coding: utf-8 -*-
from typing import Union

from cator.base.database.cursor import Cursor


class CurdDatabase(Cursor):
    """
    以下是快捷操作
    """

    def select(self, operation, params=()):
        cursor = self.execute(operation=operation, params=params)
        return cursor.fetchall()

    def select_one(self, operation, params=()):
        cursor = self.execute(operation=operation, params=params)
        return cursor.fetchone()

    def update(self, operation, params=()):
        cursor = self.execute(operation=operation, params=params)
        return cursor.rowcount

    def delete(self, operation, params=()):
        cursor = self.execute(operation=operation, params=params)
        return cursor.rowcount

    def insert(self, operation, params: Union[list, dict]):
        cursor = self.execute(operation=operation, params=params)
        return cursor.rowcount

    def insert_one(self, operation, params: Union[tuple, dict] = ()):
        cursor = self.execute(operation=operation, params=params)
        return cursor.lastrowid
