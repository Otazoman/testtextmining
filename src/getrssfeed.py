#!/usr/bin/env python3
# coding: utf-8
import csv
import collections
import datetime
import json
import pprint
import sys
from concurrent.futures import ThreadPoolExecutor
import time
import traceback

import feedparser
import japanesenormaraizer as jn
import mongo_crud as mon


def getfeedurl(infile):
    """
    CSVファイルからフィードURL、カテゴリ、タイトル一覧を取得する

    """
    try:
        result=[[]]
        with open(infile, "r") as f:
            data = csv.reader(f)
            h = next(data)

            result =[ r for r in data if r ]
        return result
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def rssparse(feedurl,name,category):
    """
    RSSフィードからＮ時間前のタイトルと概要と更新日時を取得する。
    """
    try:
        td = datetime.timedelta(hours=-24)    
        ref_time = datetime.datetime.now() + td
        rt = ref_time.timetuple()
        result=[]
        keys = ['name','category','title','description','link','updated']
        feed = feedparser.parse(feedurl, 
                response_headers={"content-type": "text/xml; charset=utf-8"})
        for x in feed.entries:
            if x is not None:
               if hasattr(x, 'title') and \
                  hasattr(x, 'description') and \
                  hasattr(x, 'href') and \
                  hasattr(x, 'updated_parsed'):
                         if rt < x.updated_parsed:
                            n = name
                            c = category
                            t = jn.strnormaraizer(x.title)
                            d = jn.strnormaraizer(x.description)
                            l = x.links[0].href
                            u = time.strftime('%Y-%m-%d %H:%M:%S',
                                        x.updated_parsed)
                            values = [n,c,t,d,l,u]
                            o = dict(zip(keys,values))
                            result.append(o)
        if result:
           return result
        else:
            return
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def data_output(output_file,from_feed_data,mode):
    """
    取得したRSSデータを出力する
    """
    try:
        mongo = mon.MongoInsert('cr_tohonokai', 'rss_article')
        if mode=='file':
           if from_feed_data:
              with open(output_file,'w') as f:
                   f.write(json.dumps(from_feed_data, indent=2, 
                       ensure_ascii=False))
        elif mode=='db':
             for media in from_feed_data:
                 #mongo.insert_many(media)
                 if media:
                    for d in media:
                        mongo.insert_one(d)
                 #       print(d)




    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def main():
    """
    主処理
    RSSフィードCSVを読込んでその内容をJSONで出力する。

    """
    try:
        start_t = time.perf_counter()
        print('Please input inputfilename')
        input_file = input('>>')
        if not input_file:
           print("Please input inputfilename!!")
           sys.exit()

        print('Please input outputfilename')
        output_file = input('>>')
        if not output_file:
           mode = 'db'
           #output_file = input_file + ".json"
           #print('outputfilename auto generate {0}'.format(output_file))
        else:
           mode = 'file'
           output_file = output_file +".json"

        feedlists = getfeedurl(input_file)
        size = len(feedlists)
        print('RSSフィード数:{0}件'.format(size))
        names = [x[0] for x in feedlists]
        urls = [x[1] for x in feedlists]
        categories = [x[2] for x in feedlists]
        wk=20
        out=[]
        #マルチスレッドでRSSを取得する
        with ThreadPoolExecutor(max_workers=wk) as executor:
             r = list(executor.map(rssparse, urls,names,categories))
        out=[ e for e in r if e]
        #データ出力
        data_output(output_file,out,mode)
        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
        
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
