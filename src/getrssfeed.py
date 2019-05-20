#!/usr/bin/env python3
# coding: utf-8
import csv
import collections
import json
#from multiprocessing import Pool
import pprint
import sys
from concurrent.futures import ThreadPoolExecutor
import time
import traceback

import feedparser

def getfeedurl(infile):
    """
    CSVファイルからフィード一覧を取得する

    """
    try:
        result=[]
        with open(infile, newline = "") as f:
            for r in csv.reader(f):
                result.append(r[1])
        del result[0]
        return result
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def rssparse(feedurl):
    """
    RSSフィードからタイトルと概要と更新日時を取得する。
    """
    try:
        result=[]
        keys = ['title','description','link','updated']
        feed = feedparser.parse(feedurl, response_headers={"content-type": "text/xml; charset=utf-8"})
        for x in feed.entries:
            if x is not None:
               if hasattr(x, 'title') and \
                  hasattr(x, 'description') and \
                  hasattr(x, 'href') and \
                  hasattr(x, 'updated_parsed'):
                  values = [x.title,x.description,x.links[0].href,time.strftime('%Y-%m-%d %H:%M:%S', x.updated_parsed)]
                  o = dict(zip(keys,values))
                  result.append(o)
        return result
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def main():
    """
    主処理
    第1引数から入力ファイル、第2引数から出力ファイルを取得する
    """
    try:
        start_t = time.perf_counter()
        input_file = sys.argv[1]
        output_file= sys.argv[2]
        urls = getfeedurl(input_file)
        size = len(urls)
        print('RSSフィード数:{0}件'.format(size))
        wk=10
        with ThreadPoolExecutor(max_workers=wk) as executor:
             out = list(executor.map(rssparse, urls))
        with open(output_file,'w') as f:
             f.write(json.dumps(out, indent=2, ensure_ascii=False))
        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()

