# -*- coding: utf-8 -*-

from typing import Union, Dict, List

from cator.sql import SqlBuilder
from ..sql import SqlUtil


class Table(object):

    def __init__(self, database, table_name: str, primary_key: str = 'id'):
        self.database = database
        self.table_name = table_name
        self.primary_key = primary_key

    @property
    def columns(self) -> List:
        """返回列名"""
        raise NotImplementedError

    @property
    def total(self) -> int:
        """返回表数据行数"""
        sql = (SqlBuilder()
               .select('count(*) as total')
               .from_(self.backquote_table_name)
               .build()
               )
        row = self.database.select_one(sql=sql)
        return row['total']

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
               .insert_into(self.backquote_table_name)
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
               .insert_into(self.backquote_table_name)
               .values(data.keys())
               .build()
               )

        return self.database.insert_one(sql=sql, params=data)

    def delete_by_id(self, uid) -> int:
        """
        :param uid: primary key value
        :return: affect row count
        """
        sql = (SqlBuilder()
               .delete_from(self.backquote_table_name)
               .where(self.primary_key_equal_sql)
               .build()
               )
        params = {self.primary_key: uid}

        return self.database.delete(sql=sql, params=params)

    def update_by_id(self, uid, data) -> int:
        """
        :param uid: primary key value
        :param data: dict
        :return: affect row count
        """
        sql = (SqlBuilder()
               .update(self.backquote_table_name)
               .set(data.keys())
               .where(self.primary_key_equal_sql)
               .build()
               )

        params = {**data, self.primary_key: uid}

        return self.database.update(sql=sql, params=params)

    def select_by_id(self, uid) -> Dict:
        """
        :param uid: primary key value
        :return: row dict
        """
        sql = (SqlBuilder()
               .select('*')
               .from_(self.backquote_table_name)
               .where(self.primary_key_equal_sql)
               .build()
               )

        params = {self.primary_key: uid}

        return self.database.select_one(sql=sql, params=params)

    @property
    def primary_key_equal_sql(self):
        return SqlUtil.column_operation_sql(column=self.primary_key, operator='=')

    @property
    def backquote_table_name(self):
        return SqlUtil.backquote(self.table_name)
