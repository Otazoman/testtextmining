#!/usr/bin/env python3
# coding: utf-8
import csv
import collections
import json
import pprint
import re
import sys
from concurrent.futures import ThreadPoolExecutor
import time
import traceback

import emoji
import feedparser
import neologdn


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


def strnormaraizer(str):
    """
    wikipediaデータの日本語を正規化する
    """
    try:
        s = neologdn.normalize(str)
        s = re.sub(
                r'(http|https)://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?',
                "",s
              )
        s = re.sub("<.*?>","",s)
        s = re.sub(r'(\d)([,.])(\d+)', r'\1\3', s)
        s = re.sub(r'[!-/:-@[-`{-~]', r' ', s)
        s = re.sub(u'[■-♯]', ' ', s)
        s = re.sub(r'(\d)([,.])(\d+)', r'\1\3', s)
        s = re.sub(r'\d+', '0', s)
        s = re.sub(r'0', '', s)
        s = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in s])
        return s
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))


def rssparse(feedurl,name,category):
    """
    RSSフィードからタイトルと概要と更新日時を取得する。
    """
    try:
        result=[]
        keys = ['name','category','title','description','link','updated']
        feed = feedparser.parse(feedurl, response_headers={"content-type": "text/xml; charset=utf-8"})
        for x in feed.entries:
            if x is not None:
               if hasattr(x, 'title') and \
                  hasattr(x, 'description') and \
                  hasattr(x, 'href') and \
                  hasattr(x, 'updated_parsed'):
                         n = name
                         c = category
                         t = strnormaraizer(x.title)
                         d = strnormaraizer(x.description)
                         l = x.links[0].href
                         u = time.strftime('%Y-%m-%d %H:%M:%S',x.updated_parsed)
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
           output_file = input_file + ".json"
           print('outputfilename auto generate {0}'.format(output_file))
        else:
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
        #ファイルに書込
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