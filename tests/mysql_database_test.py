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

    def test_execute(self):
        cursor = self.db.execute("show tables")
        print(cursor.fetchall())

    def test_select(self):
        rows = self.db.select('select * from person limit :limit', {'limit': 1})
        print(rows)

    def test_select_one(self):
        row = self.db.select_one('select * from person where id = :id', {'id': 5})
        print(row)
        # {'id': 5, 'name': 'Tom', 'age': 23}

    def test_insert(self):
        data = [{'name': 'Tom', 'age': 23}]
        row_count = self.db.insert("insert into person (`name`, `age`) values (:name, :age)", data)
        print(row_count)  # 1

    def test_insert_one(self):
        data = {'name': 'Tom', 'age': 23}
        row_id = self.db.insert_one("insert into person (`name`, `age`) values (:name, :age)", data)
        print(row_id)  # 5

    def test_update(self):
        sql = "update person set name = :name where id = :id"
        data = {
            'name': 'Jack',
            'id': 1
        }
        row_count = self.db.update(sql, data)
        print(row_count)  # 1

    def test_delete(self):
        sql = "delete from person where id = :id"
        data = {
            'id': 1
        }
        row_count = self.db.delete(sql, data)
        print(row_count)  # 1

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

        print('total', table.select_count())

    def test_table_insert_one(self):
        row_id = self.table.insert_one({'name': 'Tom', 'age': 23})
        print(row_id)  # 6
        # INSERT INTO `person` ( `name`, `age` ) VALUES ( %(name)s, %(age)s )

    def test_table_insert(self):
        data = [
            {'name': 'Tom', 'age': 23},
            {'name': 'Steve', 'age': 25}
        ]
        row_count = self.table.insert(data)
        print(row_count)  # 2
        # INSERT INTO `person` ( `age`, `name` ) VALUES ( %(age)s, %(name)s )

        # ret = self.table.insert([
        #     {'name': 'Tom', 'age': 23},
        #     {'name': 'Jack', 'age': 24},
        # ])
        # print('ret', ret)

    def test_table_delete_by_id(self):
        row_count = self.table.delete_by_id(uid=6)
        print(row_count)  # 1
        # DELETE FROM `person` WHERE `id` = %(id)s

    def test_table_update_by_id(self):
        data = {'name': 'Jackk'}
        row_count = self.table.update_by_id(uid=1, data=data)
        print(row_count)  # 1
        # UPDATE `person` SET `name` = %(name)s WHERE `id` = %(id)s

    def test_table_select_by_id(self):
        row = self.table.select_by_id(uid=5)
        print(row)  # {'id': 5, 'name': 'Tom', 'age': 23}
        # SELECT * FROM `person` WHERE `id` = %(id)s

    def test_time_out(self):
        ret = self.table.select_by_id(uid=1)
        time.sleep(4)
        ret = self.table.select_by_id(uid=2)
        print(ret)

    def test_table_select(self):
        rows = (self.table
                .where("id > ?", 1)
                .order_by("id desc")
                .limit(1)
                .select())
        # SELECT * FROM `person` WHERE id > %s ORDER BY id desc LIMIT %s
        print(rows)
        # [{'id': 9, 'name': 'Steve', 'age': 25}]

    def test_table_select_like(self):
        ret = (self.table
               .where("id like ? and id  = ?", '%tom%', 2)
               .order_by("id desc")
               .select(['id']))
        # SELECT `id` FROM `person` WHERE id like '%tom%' ORDER BY id desc
        print(ret)

    def test_table_update(self):
        row_count = (self.table
                     .where("id = ?", 1)
                     .update({'age': 24})
                     )
        # UPDATE `person` SET `age` = %s WHERE id = %s

        print(row_count)

    def test_table_delete(self):
        row_count = (self.table
                     .where("id = ?", 1)
                     .delete()
                     )
        # DELETE FROM `person` WHERE id = %s

        print(row_count)  # 0

    def test_table_count(self):
        total = (self.table
                 .where("age > ?", 10)
                 .select_count()
                 )
        print(total)  # 7
        # SELECT count(*) as total FROM `person` WHERE age > %s

    def test_table_first(self):
        ret = (self.table
               .where("id = ?", 2)
               .select_one()
               )
        # SELECT * FROM `person` WHERE id = %s LIMIT 1

        print(ret)
        # {'id': 2, 'name': 'Tom', 'age': 23}

    def test_table_select_page(self):
        query = self.table.where("age > ?", 1)

        total = query.select_count('id')
        print(total)  # 7
        # SELECT count(*)  FROM `person` WHERE age > %s

        rows = query.select_page(2, 1)
        # SELECT * FROM `person` WHERE age > %s LIMIT %s OFFSET %s
        print(rows)
        # [{'id': 3, 'name': 'Tom', 'age': 23}]

    def test_increment(self):
        row_count = self.table.where("id = ?", 4).increment('age', 1)
        # UPDATE `person` SET `age` = `age` + %s WHERE id = %s
        print(row_count)

    def test_decrement(self):
        row_count = self.table.where("id = ?", 4).decrement('age', 1)
        # UPDATE `person` SET `age` = `age` - %s WHERE id = %s
        print(row_count)