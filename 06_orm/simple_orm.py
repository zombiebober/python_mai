from functools import partial
import pytest
import sqlite3
import abc


class Field:
    field_type = "DEFAULT"

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        if instance is not None:
            instance.__dict__[self.storage_name] = value


class CharField(Field):
    field_type = 'VARCHAR'

    def __init__(self, max_length=None, min_length=None):
        self.__dict__['max_length'] = max_length
        self.__dict__['min_length'] = min_length

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError(instance, self.storage_name, str, value)
        if self.min_length is not None and self.min_length > len(value):
            raise ValueError(instance, value, self.min_length)
        elif self.max_length is not None and self.max_length < len(value):
            raise ValueError(instance, value, self.max_length)
        super().__set__(instance, value)


class IntegerField(Field):
    field_type = 'INT'

    def __init__(self, min_value=None):
        self.__dict__["min_value"] = min_value

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(instance, value)
        if self.min_value is not None and self.min_value > value:
            raise ValueError(instance, value, self.min_value)

        super().__set__(instance, value)


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):

        database = dict()
        for base in bases:
            if hasattr(base, "Meta"):
                database = base.Meta.__dict__["database"]
                setattr(cls, "create_colums", partial(database.create, name_table=name))
                setattr(cls, "select", partial(database.select, name_table=name))

        return super().__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        pass


class Model(metaclass=ModelMeta):
    @classmethod
    def get_classname(cls):  # classmethod select
        return cls.__name__

    @classmethod
    def create(cls, **kwargs):
        slf = cls()
        meta = slf._prepare_insert(**kwargs)
        cls.create_colums(colums=meta)
        return slf

    def _prepare_insert(self, **kwargs):
        meta = {}
        for key, value in kwargs.items():
            if key in self.__class__.__dict__ and isinstance(self.__class__.__dict__[key], Field):
                self.__class__.__dict__[key].__set__(self, value)
                meta[key] = self.__class__.__dict__[key].__get__(self, None)
            else:
                raise KeyError
        return meta


class Database():
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def create_tables(self, tabe: list):
        pass

    @abc.abstractmethod
    def create(self, name: str, colums: dict):
        pass

    @abc.abstractmethod
    def select(self, name: str, colums: dict):
        pass


class SqliteDatabase(Database):

    def __init__(self, db_location=':memory:'):
        self.db_location = db_location

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_location)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            self.conn.close()
            raise e

    def create_tables(self, tables: list):
        for table in tables:
            self.create_table(table)

    def create_table(self, table: Model):
        colums = [f"{key} {colums_type.field_type}"
                  for key, colums_type in table.__dict__.items()
                  if isinstance(colums_type, Field)]
        sql = "CREATE TABLE {} ({});".format(table.get_classname(), ', '.join(colums))
        self.cursor.execute(sql)
        self.conn.commit()

    def create(self, name_table: str, colums: dict):
        # arg = ','.join( "?"*len(colums))
        # sql = "INSERT INTO {} ({}) VALUES  ({});".format(name_table, arg, arg)
        # arg = [k for k in colums.keys()]+[str(v) for v in colums.values()]
        # self.cursor.execute(sql, arg)
        arg = ','.join([k for k in colums.keys()])
        val = ','.join([str(k) for k in colums.values()])
        val = [(k) for k in colums.values()]
        sql = "INSERT INTO {}({}) VALUES  ({});".format(name_table, ','.join([k for k in colums.keys()]),
                                                        ','.join(["\'{}\'".format(k) for k in colums.values()]))
        self.cursor.execute(sql)
        self.conn.commit()

    def select(self, name_table: str):
        sql = f"SELECT * FROM {name_table}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


db = SqliteDatabase(":memory:")


class BaseModel(Model):
    pass

    class Meta:
        database = db


class Advert(BaseModel):
    title = CharField(max_length=180)
    price = IntegerField(min_value=0)


db.connect()
db.create_tables([Advert])

Advert.create(title='iPhone X', price=100)
adverts = Advert.select()
assert str(adverts[0]) == "('iPhone X', 100)"
db.close()
