# -*- coding: utf-8 -*-

import logging
import unittest

import cator

logging.basicConfig(level=logging.DEBUG)


class SQLiteDatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        # autocommit 模式: isolation_level=null
        db_url = 'sqlite:///data.db'
        self.db = cator.connect(db_url)
        self.table = self.db.table('person')

    def tearDown(self) -> None:
        self.db.close()

    def test_create_table(self):
        sql = """create table if not exists person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            age int
            )
        """

        self.db.execute(sql)

    def test_table(self):
        table = self.db.table('person')

        print('total', table.total)

    def test_transaction(self):
        self.db.table('person').insert_one({'name': 'transaction-rollback'})
        self.db.rollback()
        self.db.table('person').insert_one({'name': 'transaction-commit'})
        self.db.commit()

    def test_table_insert_one(self):
        ret = self.table.insert_one({'name': 'Tom', 'age': 23})
        print('ret', ret)

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

    def test_table_select(self):
        ret = self.table.select_by_id(uid=1)
        print(ret)
