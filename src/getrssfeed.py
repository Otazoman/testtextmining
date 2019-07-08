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
                         t = strnormaraizer(x.title)
                         d = strnormaraizer(x.description)
                         l = x.links[0].href
                         u = time.strftime('%Y-%m-%d %H:%M:%S',x.updated_parsed)
                         values = [t,d,l,u]
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
    第1引数から入力ファイル、第2引数から出力ファイルを取得する
    使用例：$ python getrssfeed.py feedurl.csv output.json
    
    """
    try:
        start_t = time.perf_counter()
        #input_file = sys.argv[1]
        #output_file= sys.argv[2]
        #args
        print('Please input inputfilename')
        input_file = input('>>')
        if not input_file:
           print("Please input inputfilename!!")
           sys.exit()

        print('Please input outputfilename')
        output_file = input('>>')
        if not output_file:
           print('outputfilename auto generate')
           output_file = input_file + ".txt"

        urls = getfeedurl(input_file)
        size = len(urls)
        print('RSSフィード数:{0}件'.format(size))
        wk=20
        out=[]
        #マルチスレッドでRSSを取得する
        with ThreadPoolExecutor(max_workers=wk) as executor:
             r = list(executor.map(rssparse, urls))
        #記事が存在するもののみ抽出
        #out = fliter(lambda a: a is not None , r)
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
