import json
import pprint
import re
import sys
import traceback

import mongo_crud as mon

def main():
    try:
        print("FIND START")
        mongo = mon.MongoFind('cr_tohonokai', 'test1')
        findOne = mongo.find_one()
        print('-----------------find_One-----------------')
        print(type(findOne))
        print(findOne)
        find = mongo.find({'age':30},{'_id':0})
        print('-------------------find-------------------')
        print(type(find))
        for doc in find:
            print(doc)
        print("FIND END")

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
        
        print("INSERT START")
        mongo = mon.MongoInsert('cr_tohonokai', 'test1')
        find = mongo.find()
        print('--------------------登録前--------------------')
        for doc in find:
            print(doc)
        print('-------------------登録情報-------------------')
        result = mongo.insert_one({'name':'加藤','salary':400000})
        print(type(result))
        print(result)
        print(result.inserted_id)
        print('--------------------登録後--------------------')
        find = mongo.find()
        for doc in find:
            print(doc)
        print("INSERT END")

        print("DELETE START")
        mongo = mon.MongoDelete('cr_tohonokai', 'test1')
        print('--------------------削除前--------------------')
        find = mongo.find()
        for doc in find:
            print(doc)
        print('-------------------削除情報-------------------')
        result = mongo.delete_one({'name':'加藤'})
        print(type(result))
        print(result)
        print(result.deleted_count)

        print('--------------------削除後--------------------')
        find = mongo.find()
        for doc in find:
            print(doc)
        print("DELETE END")

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
