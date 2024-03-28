# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import DatabaseProxy

from typing import Union, Dict

from cator.base.query import Query
from cator.sql import SqlBuilder, SqlUtil


class Table(object):

    def __init__(self, database: Union["DatabaseProxy", None], table_name: str, primary_key: str = 'id'):
        self.database = database
        self.table_name = table_name
        self._table_name = SqlUtil.backquote(self.table_name)
        self.primary_key = primary_key

    def insert(self, data: Union[dict, list]) -> int:
        """
        :param data: list[dict]/dict
        :return: affect row count
        """
        if not data:
            return 0

        if isinstance(data, dict):
            columns = data.keys()
        elif isinstance(data, list):
            columns = SqlUtil.get_list_columns(data)
        else:
            raise Exception('data type must dict or list[dict]')

        sql = (SqlBuilder()
               .insert_into(self._table_name)
               .values(columns)
               .build()
               )

        return self.database.insert(sql=sql, params=data)

    def insert_one(self, data: dict) -> int:
        """
        :param data: dict
        :return: inserted row id
        """
        sql = (SqlBuilder()
               .insert_into(self._table_name)
               .values(data.keys())
               .build()
               )

        return self.database.insert_one(sql=sql, params=data)

    def delete_by_id(self, uid) -> int:
        """
        :param uid: primary key value
        :return: affect row count
        """
        return (self.new_query()
                .where("`{primary_key}` = ?".format(primary_key=self.primary_key), uid)
                .delete())

    def update_by_id(self, uid, data) -> int:
        """
        :param uid: primary key value
        :param data: dict
        :return: affect row count
        """
        return (self.new_query()
                .where("`{primary_key}` = ?".format(primary_key=self.primary_key), uid)
                .update(data))

    def select_by_id(self, uid, columns=None) -> Dict:
        """
        :param uid: primary key value
        :param columns:
        :return: row dict
        """

        return (self.new_query()
                .where("`{primary_key}` = ?".format(primary_key=self.primary_key), uid)
                .select_one(columns)
                )

    def select_one(self, columns=None) -> int:
        """return table row total count"""
        return self.new_query().select_one(columns)

    def select_count(self, column=None) -> int:
        """return table row total count"""
        return self.new_query().select_count(column)

    def select_page(self, page: int, size: int, columns=None) -> int:
        """select rows"""
        return self.new_query().select_page(page, size, columns)

    def where(self, sql, *args):
        return self.new_query().where(sql, *args)

    def new_query(self):
        return Query(self.database).from_(self.table_name)
