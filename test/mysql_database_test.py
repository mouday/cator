# -*- coding: utf-8 -*-
import logging
import time
import unittest

import cator

logging.basicConfig(level=logging.DEBUG)


class MySqlDatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        # show PROCESSLIST;
        db_url = 'mysql+reconnect://root:123456@localhost:3306/data?autocommit=true'
        self.db = cator.connect(db_url)
        self.table = self.db.table('person')

    def tearDown(self) -> None:
        self.db.close()

    def test_select(self):
        rows = self.db.select('select * from person limit :limit', {'limit': 1})

        print(rows)

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

    def test_table_delete_by_id(self):
        ret = self.table.delete_by_id(uid=6)
        print(ret)

    def test_table_update_by_id(self):
        ret = self.table.update_by_id(uid=1, data={'name': 'Jackk'})
        print(ret)

    def test_table_select_by_id(self):
        ret = self.table.select_by_id(uid=1)
        print(ret)

    def test_time_out(self):
        ret = self.table.select_by_id(uid=1)
        time.sleep(4)
        ret = self.table.select_by_id(uid=2)
        print(ret)

    def test_table_select(self):
        ret = (self.table
               .where("id > 1")
               .order_by("id desc")
               .limit(1)
               .select())
        # SELECT * FROM `person` WHERE id > 1 ORDER BY id desc LIMIT 1
        print(ret)

    def test_table_select_like(self):
        ret = (self.table
               .where("id like '%tom%'")
               .order_by("id desc")
               .select('`id`'))
        # SELECT `id` FROM `person` WHERE id like '%tom%' ORDER BY id desc
        print(ret)

    def test_table_update(self):
        ret = (self.table
               .where("id = 1")
               .update({'age': 24})
               )
        # UPDATE `person` SET `age` = %(age)s WHERE id = 1

        print(ret)

    def test_table_delete(self):
        ret = (self.table
               .where("id = 1")
               .delete()
               )
        # DELETE FROM `person` WHERE id = 1

        print(ret)

    def test_table_count(self):
        ret = (self.table
               .where("id = 1")
               .count()
               )
        # SELECT count(*) as total FROM `person` WHERE id = 1

        print(ret)

    def test_table_first(self):
        ret = (self.table
               .where("id = 2")
               .first()
               )
        # SELECT * FROM `person` WHERE id = 2 LIMIT 1

        print(ret)
        # {'id': 2, 'name': 'Tom', 'age': 23}
