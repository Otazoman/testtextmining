import datetime
import json
import pprint
import re
import sys
import traceback
from bson.objectid import ObjectId

import mongo_crud as mon

def insert_mongo():
    try:
        print("INSERT START")
        mongo = mon.MongoInsert('cr_tohonokai', 'test1')
        find = mongo.find({'_id':0})
        print('--------------------登録前--------------------')
        for doc in find:
            print(doc)
        insert_data = []
        i = 1
        for i in range(5):
            odict = {'new_column1': 'new_value' + str(i),
                     'new_column2': 'A-' + str(i),
                     'date_column': datetime.datetime.utcnow()
                     }
            insert_data.append(odict)
            i+=1
        result = mongo.insert_many(insert_data)
        print('-------------------登録情報-------------------')
        print(type(result))
        print(result)
        print('----------------------------------------------')
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def find_mongo():
    try:
        tz = datetime.timezone.utc
        td = datetime.timedelta(hours=-1)
        start = datetime.datetime.now(tz) + td
        end = datetime.datetime.now(tz)
        
        print(type(start))
        print(start)
        print(type(end))
        print(end)

        print("FIND START")
        #mongo = mon.MongoFind('cr_tohonokai', 'test1')
        mongo = mon.MongoFind('cr_tohonokai', 'rss_article')
        
        find = mongo.find({'_id':0})
        print('--------------------全件--------------------')
        #for doc in find:
        #    print(doc)
        #print('---------------------------------------------') 
#        find = mongo.find({'_id':0,'name':1,'category':1,'title':1,
#            'addlabel':1,'labelstat':1,'updated':1},filter={'dupukey': {'$ne':"DUPULECATE"}}) 
        i = 0
        find = mongo.find({'_id':0,'name':1,'category':1,'title':1,
            'addlabel':1,'labelstat':1,'poststatus':1,'updated':1},filter={'poststatus':{'$ne':'POSTED'}}) 
        for doc in find:
            print(doc)
            i +=1
        print('---------------------------------------------') 
        print('レコード：'+str(i)+'件')
        cmongo = mon.MongoCount('cr_tohonokai', 'rss_article')
        cnt = cmongo.count({})
        print('全件'+str(cnt)+'件')

        #find = mongo.find(filter={'updated':{'$gte': start,'$lt': end}},
        #        projection={'_id':0,})
        #print('--------------------条件--------------------')
        #for doc in find:
        #    print(doc)
        

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def delete_mongo():
    try:
        print("DELETE START")
        mongo = mon.MongoDelete('cr_tohonokai', 'test1')
        print('--------------------削除前--------------------')
        find = mongo.find()
        for doc in find:
            print(doc)
        print('-------------------削除情報-------------------')
        result = mongo.delete_one({'age': 100})

        print('--------------------削除後--------------------')
        find = mongo.find()
        for doc in find:
            print(doc)
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))        
        
def update_mongo():
    try:
        print("UPDATE START")
        mongo = mon.MongoUpdate('cr_tohonokai', 'test1')
        find = mongo.find()
        for doc in find:
            print(doc)
        update = mongo.update_one({"new_column2": '/.*2$/'}, {'$set':{"new_Column2":"D9992"}})
        print('更新件数：' + str(update.matched_count))
        find = mongo.find()
        for doc in find:
            print(doc)
        print("UPDATE END")
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        
def main():
    try:
        
        #insert_mongo()
        find_mongo()

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
