# -*- coding: utf-8 -*-
import logging
import unittest

from playhouse.db_url import connect
from cator.peewee import register_dict_database

register_dict_database()

logging.basicConfig(level=logging.DEBUG)


class PeeweeDictDatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        # show PROCESSLIST;
        db_url = 'mysql+dict://root:123456@localhost:3306/data'
        self.db = connect(db_url)

    def tearDown(self) -> None:
        self.db.close()

    def test_select(self):
        rows = self.db.select('select * from person limit 1')
        print(rows)
        # [{'id': 1, 'name': 'Tom'}]

        row = self.db.select_one('select * from person limit 1')
        print(row)

        print(self.db.table('person').columns)
        print(self.db.table('person').total)
        print(self.db.table('person').select_by_id(11))
