# -*- coding: utf-8 -*-
import time
import unittest

import cator
import logging

logging.basicConfig(level=logging.DEBUG)

import playhouse.db_url


class MySqlDatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        # show PROCESSLIST;
        db_url = 'mysql://root:123456@localhost:3306/data?autocommit=true'
        self.db = cator.connect(db_url)
        print(self.db.tables)
        self.table = self.db.table('person')

    def tearDown(self) -> None:
        self.db.close()

    def test_create_table(self):
        sql = """create table if not exists person (
            id int PRIMARY KEY auto_increment,
            name varchar(20),
            age int
            )
        """

        self.db.execute(sql)

    def test_table(self):
        table = self.db.table('person')

        print('columns', self.table.columns)

        print('total', table.total)

    def test_table_insert_one(self):
        ret = self.table.insert_one({'name': 'Tom', 'age': 23})
        print('ret', ret)
        time.sleep(20)

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
