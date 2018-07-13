# coding:utf-8
from db.config import db
import pymysql
from .exception import ConnectDBError, AuthDBError
from pymongo import MongoClient


class DBMySql:

    def __init__(self):
        try:
            self.conn = pymysql.Connect(
                host=db['HOST'],
                port=db['PORT'],
                username=db['username'],
                passwd=db['password'],
                db=db['db'],
                charset=db['charset']
            )
        except pymysql.OperationalError:
            raise ConnectDBError
        self.cursor = self.conn.cursor()

    def find(self, table, **kwargs):
        pass

    def save(self, table, **kwargs):
        pass

    def delete(self, table, **kwargs):
        pass

    def create_table(self, table, **kwargs):
        pass

    def update(self, table, **kwargs):
        pass

    def create_or_update(self, table, **kwargs):
        pass


class DBMongo:

    def __init__(self):
        try:
            self.client = MongoClient(host=db['HOST'], port=db['PORT'])
        except:
            raise ConnectDBError
        self.db = self.client.get_database(name=db['db'])
        if db['username'] and db['password']:
            try:
                self.db.authenticate(name=db['username'], password=db['password'])
            except:
                raise AuthDBError

    def find(self, collection, data):
        coll = self.db.get_collection(name=collection)
        ret = coll.find(data)
        if ret.count() == 1:
            return ret[0]
        elif ret.count() == 0:
            return False
        else:
            return list(ret)

    def save(self, collection, data):
        coll = self.db.get_collection(name=collection)
        coll.insert_one(data)

    def update(self, collection, condition, data):
        coll = self.db.get_collection(name=collection)
        coll.update(condition, {'$set': data})


class Operation:

    def __init__(self):
        if db['name'] == 'mysql':
            self.db = DBMySql()
        elif db['name'] == 'mongodb':
            self.db = DBMongo()
        else:
            pass
