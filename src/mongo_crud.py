from pymongo import MongoClient
from pymongo import DESCENDING
from pymongo import ASCENDING
import sys
import yaml


""" Connect """
def connDB(self, dbName, collectionName):
    try:
        with open('../config/db_config.yml', 'r') as yml:
             config = yaml.safe_load(yml)
             self.client = MongoClient(config['host'],
                                       username=config['username'],
                                       password=config['password'],
                                       authSource=dbName,
                                       authMechanism='SCRAM-SHA-1')
             self.db = self.client[dbName]
             self.collection = self.db.get_collection(collectionName)
             return self.collection
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

""" Find """
class MongoFind(object):
    def __init__(self, dbName, collectionName):
        self.collection = connDB(self, dbName, collectionName)

    def find_one(self, projection=None,filter=None, sort=None):
        return self.collection.find_one(projection=projection,filter=filter,sort=sort)

    def find(self, projection=None,filter=None, sort=None):
        return self.collection.find(projection=projection,filter=filter,sort=sort)

""" Update """
class MongoUpdate(object):
    def __init__(self, dbName, collectionName):
        self.collection = connDB(self, dbName, collectionName)

    def find(self, projection=None,filter=None, sort=None):
        return self.collection.find(projection=projection,filter=filter,sort=sort)

    def update_one(self, filter, update):
        return self.collection.update_one(filter,update)

    def update_many(self, filter, update):
        return self.collection.update_many(filter,update)

    def replace_one(self, filter, replacement):
        return self.collection.replace_one(filter, replacement)

    def find_one_and_replace(self, filter, replacement):
        return self.collection.find_one_and_replace(filter, replacement)

""" Insert """
class MongoInsert(object):
    def __init__(self, dbName, collectionName):
        self.collection = connDB(self, dbName, collectionName)

    def find(self, projection=None,filter=None, sort=None):
        return self.collection.find(projection=projection,filter=filter,sort=sort)

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def insert_many(self, documents):
        return self.collection.insert_many(documents)

""" Delete """
class MongoDelete(object):
    def __init__(self, dbName, collectionName):
        self.collection = connDB(self, dbName, collectionName)

    def find(self, projection=None,filter=None, sort=None):
        return self.collection.find(projection=projection,filter=filter,sort=sort)

    def delete_one(self, filter):
        return self.collection.delete_one(filter)

    def delete_many(self, filter):
        return self.collection.delete_many(filter)

    def find_one_and_delete(self, filter):
        return self.collection.find_one_delete(filter)

