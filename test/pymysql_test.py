# -*- coding: utf-8 -*-
import logging
import unittest

import pymysql
from cator import DatabaseProxy

logging.basicConfig(level=logging.DEBUG)


class PyMysqlDatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '123456',
            'database': 'data',
            'port': 3306
        }
        connection = pymysql.connect(**config)
        self.db = DatabaseProxy(connection)
        self.table = self.db.table('person')

    def tearDown(self) -> None:
        self.db.close()

    def test_select(self):
        rows = self.db.select('select * from person limit :limit', {'limit': 1})
        print(rows)

        rows = self.db.select('select * from person limit %(limit)s', {'limit': 1})
        print(rows)

        rows = self.db.select('select * from person limit 1')
        print(rows)
        # [{'id': 1, 'name': 'Tom'}]

        row = self.db.select_one('select * from person limit 1')
        print(row)

        print(self.db.table('person').total)
        print(self.db.table('person').select_by_id(11))

    def test_table(self):
        table = self.db.table('person')

        print('total', table.total)

    def test_table_insert_one(self):
        ret = self.table.insert_one({'name': 'Tom', 'age': 23})
        print('ret', ret)
        # time.sleep(20)

    def test_table_insert(self):
        ret = self.table.insert(
            {'name': 'Tom', 'age': 23}
        )
        print('ret', ret)

        ret = self.table.insert([
            {'name': 'Tom', 'age': 23},
            {'name': 'Jack', 'age': 24},
        ])
        print('ret', ret)

    def test_table_delete(self):
        ret = self.table.delete_by_id(uid=6)
        print(ret)

    def test_table_update(self):
        ret = self.table.update_by_id(uid=1, data={'name': 'Jackk'})
        print(ret)
