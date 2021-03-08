# Cator

![PyPI](https://img.shields.io/pypi/v/cator.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/cator)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cator)
![PyPI - License](https://img.shields.io/pypi/l/cator)

- Github: [https://github.com/mouday/cator](https://github.com/mouday/cator)
- Pypi: [https://pypi.org/project/cator](https://pypi.org/project/cator)

## 简介
封装了mysql和sqlite，用于零时执行一些脚本，项目中使用

返回数据以dict字典为主，若要修改返回值类型，可以通过继承修改

支持4种占位符：

```
mysql风格： %s   %(key)s
sqlite风格：?    :key 
```

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

    @property
    def in_transaction(self):
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


## 注意问题

1. 使用时需注意链接超时问题
2. cator支持了autocommit自动提交，默认关闭，如有需要可以打开，
3. 如果需要执行事务就需要关闭自动提交


cator基于以下模块进行改进

1. myquery
2. aquery
3. puremysql
4. pythink
