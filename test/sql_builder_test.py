# -*- coding: utf-8 -*-


import unittest

from cator.sql.sql_builder import SqlBuilder
from cator.sql.sql_util import SqlUtil


class SqlBuilderTest(unittest.TestCase):

    def test_1(self):
        sql = (SqlBuilder()
               .select_from('table')
               .where(SqlUtil.column_operation_sql('name'))
               .build()
               )

        # SELECT FROM table WHERE `name` = %(name)s
        ret = 'SELECT FROM table WHERE `name` = %(name)s'
        self.assertEqual(sql, ret)

    def test_2(self):
        in_sql, data = SqlUtil.column_in(column='age', list_params=['1', '2', '3'])

        print(data)

        sql = (SqlBuilder()
               .select_from('table')
               .where(SqlUtil.column_operation_sql('name'))
               .and_(SqlUtil.column_operation_sql('age', operator='>'))
               .and_('age')
               .in_(in_sql)
               .build()
               )

        ret = 'SELECT FROM table WHERE `name` = %(name)s AND `age` > %(age)s AND age IN ( %(age-0)s, %(age-1)s, %(age-2)s )'

        self.assertEqual(sql, ret)

    def test_3(self):
        sql = (SqlBuilder()
               .delete_from('table')
               .where(SqlUtil.column_operation_sql('name'))
               .build())

        # DELETE FROM table WHERE `name` = %(name)s
        ret = 'DELETE FROM table WHERE `name` = %(name)s'
        self.assertEqual(sql, ret)

    def test_4(self):
        sql = (SqlBuilder()
               .update('table')
               .set(['name', 'age'])
               .where(SqlUtil.column_operation_sql('id'))
               .build())
        # UPDATE table SET `name` = %(name)s, `age` = %(age)s
        ret = 'UPDATE table SET `name` = %(name)s, `age` = %(age)s WHERE `id` = %(id)s'
        self.assertEqual(sql, ret)

    def test_5(self):
        sql = (SqlBuilder()
               .insert_into('table')
               .values(['name', 'age'])
               .build())

        # INSERT INTO table ( `name`, `age` ) VALUES ( %(name)s, %(age)s )
        ret = 'INSERT INTO table ( `name`, `age` ) VALUES ( %(name)s, %(age)s )'
        print(sql)
        self.assertEqual(sql, ret)
