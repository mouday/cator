# Cator

![PyPI](https://img.shields.io/pypi/v/cator.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/cator)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cator)
![PyPI - License](https://img.shields.io/pypi/l/cator)

- Github: [https://github.com/mouday/cator](https://github.com/mouday/cator)
- Pypi: [https://pypi.org/project/cator](https://pypi.org/project/cator)

## 简介
支持 mysql和sqlite数据库

返回数据统一为dict 字典

无论使用什么数据库驱动都支持4种占位符：

| paramstyle | support | Meaning | example|
| - | - | - | - |
| qmark | OK | Question mark style | ...WHERE name=? |
| numeric   | - | Numeric, positional style | ...WHERE name=:1 |
| named | OK | Named style | ...WHERE name=:name |
| format    | OK | ANSI C printf format codes | ...WHERE name=%s |
| pyformat | OK | Python extended format codes | ...WHERE name=%(name)s |


## 安装
```bash
pip install cator
```

## 使用示例

指定 autocommit 模式

```python
import cator

# mysql
db_url = "mysql://root:123456@127.0.0.1:3306/data?charset=utf8&autocommit=true"

# sqlite
db_url = 'sqlite:///data.db?isolation_level=null'

# open Database
db = cator.connect(db_url)

# close
db.close()
```

## 接口

Database类

```python
class Database:
    @property
    def tables(self):
        pass

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
        """返回cursor 对象"""

    def connect(self):
        """连接数据库"""

    def close(self):
        """关闭连接"""
        
    def commit(self):
        pass

    def rollback(self):
        pass

```

Table 类

```python
class Table:

    @property
    def columns(self):
        pass
        
    @property
    def total(self):
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

```

## 扩展 peewee

通过`DictMySQLDatabase`类，使得peewee原生sql查询进行增强

```python

from peewee import MySQLDatabase
from cator.peewee import DictMySQLDatabase

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'data',
    'charset': 'utf8mb4',
}

# replace MySQLDatabase to DictMySQLDatabase
# db = MySQLDatabase(**config)
db = DictMySQLDatabase(**config)

```

增强的方法

```python
from peewee import MySQLDatabase


class DictMySQLDatabase(MySQLDatabase):
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

    def query(self, sql, params=None):
        pass
```

## 注意问题

1. 使用时需注意链接超时问题
2. cator支持了autocommit自动提交，默认关闭，如有需要可以打开，
3. 如果需要执行事务就需要关闭自动提交


cator基于以下模块进行了改进

1. myquery
2. aquery
3. puremysql
4. pythink
