# Cator

## 简介
封装了mysql和sqlite，用于零时执行一些脚本，如果项目中使用




## 安装
```bash
pip install cator
```

## 使用示例

```python
import cator

# mysql
db_url = "mysql://root:123456@127.0.0.1:3306/data?charset=utf8&autocommit=true"

# sqlite
db_url = 'sqlite:///data.db?autocommit=true'

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
