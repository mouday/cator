# Cator

![PyPI](https://img.shields.io/pypi/v/cator.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/cator)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cator)
![PyPI - License](https://img.shields.io/pypi/l/cator)

- Github: [https://github.com/mouday/cator](https://github.com/mouday/cator)
- Pypi: [https://pypi.org/project/cator](https://pypi.org/project/cator)
- gitee: [https://gitee.com/mouday/cator](https://gitee.com/mouday/cator)

## 简介

支持 mysql和sqlite数据库, 在现有连接对象Connection 基础上进行增强

返回数据统一为dict 字典

## 安装

```bash
pip install cator
```

支持的mysql连接库（任选其一即可）：
- pymysql
- mysql-connector-python
- mysqlclient

## 使用示例

### 1、获取新的连接Database 对象 

```python
import cator

# mysql 
db_url = "mysql://root:123456@127.0.0.1:3306/data?charset=utf8&autocommit=true"

# open Database
db = cator.connect(db_url)

# close
db.close()
```

支持的连接url，其他参数可参考所使用的链接库的文档

```bash
# mysql autocommit=true参数指定自动提交
mysql://root:123456@127.0.0.1:3306/data?charset=utf8&autocommit=true

# mysql+reconnect 模式可以指定断线重连
mysql+reconnect://root:123456@127.0.0.1:3306/data?autocommit=true

# sqlite
sqlite:///data.db?isolation_level=null
```

### 2、Database对象 CURD使用示例

创建测试表

```sql
create table if not exists person (
    id int PRIMARY KEY auto_increment,
    name varchar(20),
    age int
)
```

CURD

```python
# 执行原样sql 返回cursor对象
cursor = db.execute("show tables")


# insert
sql = "insert into person (`name`, `age`) values (:name, :age)"
data = [{'name': 'Tom', 'age': 23}]
row_count = db.insert(sql, data)
print(row_count) # 1


# insert_one
sql = "insert into person (`name`, `age`) values (:name, :age)"
data = {'name': 'Tom', 'age': 23}
row_id = db.insert_one(sql, data)
print(row_id) # 5


# select
sql = 'select * from person limit :limit'
data = {'limit': 1}
rows = db.select(sql, data)
# [{'id': 2, 'name': 'Tom', 'age': 23}]


# select_one
sql = 'select * from person where id = :id'
data = {'id': 5}
row = db.select_one(sql, data)
print(row)
# {'id': 5, 'name': 'Tom', 'age': 23}


# update
sql = "update person set name = :name where id = :id"
data = {
    'name': 'Jack',
    'id': 1
}
row_count = db.update(sql, data)
print(row_count) # 1


# delete
sql = "delete from person where id = :id"
data = {
    'id': 1
}
row_count = db.delete(sql, data)
print(row_count) # 1
```

### Table操作

Table 类提供了一系列的简化操作

> 注意：使用table操作，仅支持`?`或者`%s`作为占位符

```python
# 获取 Table 对象
table = db.table('person')


# insert_one
data = {'name': 'Tom', 'age': 23}
row_id = table.insert_one(data)
print(row_id) # 6
# INSERT INTO `person` ( `name`, `age` ) VALUES ( %(name)s, %(age)s )


# insert
data = [
    {'name': 'Tom', 'age': 23},
    {'name': 'Steve', 'age': 25}
]
row_count = table.insert(data)
print(row_count) # 2
# INSERT INTO `person` ( `age`, `name` ) VALUES ( %(age)s, %(name)s )


# update_by_id
data = {'name': 'Jackk'}
row_count = table.update_by_id(uid=1, data=data)
print(row_count) # 1
# UPDATE `person` SET `name` = %(name)s WHERE `id` = %(id)s


# delete_by_id
row_count = table.delete_by_id(uid=6)
print(row_count) # 1
# DELETE FROM `person` WHERE `id` = %(id)s


# where select
rows = (table
       .where("id > ?", 1)
       .order_by("id desc")
       .limit(1)
       .select())
# SELECT * FROM `person` WHERE id > %s ORDER BY id desc LIMIT %s
print(rows)
# [{'id': 9, 'name': 'Steve', 'age': 25}]


# select_by_id
row = table.select_by_id(uid=5)
print(row) # {'id': 5, 'name': 'Tom', 'age': 23}
# SELECT * FROM `person` WHERE `id` = %(id)s


# select count
total = table.select_count()
print(total) # 5
# SELECT count(*) as total FROM `person`

# where select_one
ret = (table
       .where("id = ?", 2)
       .select_one()
       )
# SELECT * FROM `person` WHERE id = 2 LIMIT 1

print(ret)
# {'id': 2, 'name': 'Tom', 'age': 23}


# where select count
total = (table
         .where("age > ?", 10)
         .select_count()
         )
print(total)  # 7
# SELECT count(*) as total FROM `person` WHERE age > %s


# where delete
row_count = (table
             .where("id = ?", 1)
             .delete()
             )
# DELETE FROM `person` WHERE id = %s

print(row_count) # 0

# where update
row_count = (table
       .where("id = ?", 1)
       .update({'age': 24})
       )
# UPDATE `person` SET `age` = %s WHERE id = %s
print(row_count) # 1


# select page
query = table.where("age > ?", 1)

total = query.select_count('id')
print(total)  # 7
# SELECT count(`id`) FROM `person` WHERE age > %s

rows = query.select_page(2, 1)
# SELECT * FROM `person` WHERE age > %s LIMIT %s OFFSET %s
print(rows)
# [{'id': 3, 'name': 'Tom', 'age': 23}]

```
 
## 2、扩展现有连接

`DatabaseProxy`类接收一个`Connection`对象，只需要实现以下4个方法即可

```python
class Connection(ABC):
    def close(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        pass

```

#### 2-1、扩展 peewee

通过`DatabaseProxy`类，使得peewee原生sql查询进行增强

```python

from peewee import MySQLDatabase
from cator import DatabaseProxy


config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'data',
    'charset': 'utf8mb4',
}

db = MySQLDatabase(**config)

# use cator database proxy
db_proxy = DatabaseProxy(db)

```

#### 2-2、扩展 pymysql

```python
import pymysql
from cator import DatabaseProxy

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'data',
    'port': 3306
}

connection = pymysql.connect(**config)
proxy_db = DatabaseProxy(connection)

rows = proxy_db.select('select * from person where id = :id', {'id': 15})
print(rows)
proxy_db.close()

```

## 支持的占位符

无论使用什么数据库驱动都支持4种占位符：

| paramstyle | support | Meaning | example |
| - | - | - | - |
| qmark | OK | Question mark style | `...WHERE name=?` |
| numeric | - | Numeric, positional style | `...WHERE name=:1` |
| named | OK | Named style | `...WHERE name=:name` |
| format | OK | ANSI C printf format codes | `...WHERE name=%s` |
| pyformat | OK | Python extended format codes | `...WHERE name=%(name)s` |


## 接口

Database类

```python
class DatabaseProxy:
    def table(self, table_name):
        pass
    
    def select(self, operation, params=()):
        pass

    def select_one(self, operation, params=()):
        pass

    def update(self, operation, params=()):
        pass

    def delete(self, operation, params=()):
        pass

    def insert(self, operation, params: Union[list, dict]):
        pass

    def insert_one(self, operation, params: Union[tuple, dict] = ()):
        pass

    def before_execute(self, operation, params=None):
        pass

    def after_execute(self, cursor):
        pass

    def execute(self, operation, params=None):
        pass
    
    def cursor(self, *args, **kwargs):
        """return cursor object"""

    def connect(self):
        """connect database"""

    def close(self):
        """close connection"""
        
    def commit(self):
        pass

    def rollback(self):
        pass

```

Table 类

```python
class Table:

    def count(self):
        pass

    def insert(self, data: Union[dict, list]):
        pass
        
    def insert_one(self, data: dict):
        pass
        
    def delete_by_id(self, uid):
        pass
        
    def update_by_id(self, uid, data):
        pass
        
    def select_by_id(self, uid):
        pass
    
    def where(self, sql, *args):
        pass
```

## 显示sql日志

```python
import logging

logger = logging.getLogger('cator')
logger.setLevel(level=logging.DEBUG)
```

## 注意问题

1. 使用时需注意链接超时问题
2. cator支持了autocommit自动提交，默认关闭，如有需要可以打开，
3. 如果需要执行事务就需要关闭自动提交

cator基于以下模块进行了改进

1. myquery：https://github.com/mouday/myquery
2. aquery：https://github.com/mouday/aquery
3. puremysql https://github.com/mouday/puremysql
4. pythink https://github.com/mouday/pythink
