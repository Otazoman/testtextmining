#!/usr/bin/env python3
# coding: utf-8
import csv
import collections
import json
from multiprocessing import Pool
import pprint
import re
import sys
import time
import traceback

import feedparser
import MeCab
from pytrends.request import TrendReq


def gtrend_get(urls):
    """
    Googleトレンドのデータを取得する。
    """
    try:
        result=[]
        keys = [
                 'title','ht_approx_traffic','ht_news_item_title',
                 'published_parsed'
               ]
        feed = feedparser.parse(urls)
        for x in feed.entries:
            if x is not None:
               if hasattr(x, 'title') and \
                  hasattr(x, 'ht_approx_traffic') and \
                  hasattr(x, 'ht_news_item_title') and \
                  hasattr(x, 'published_parsed'):
                  values = [
                             x.title,
                             x.ht_approx_traffic.replace('+',''),
                             x.ht_news_item_title,
                             time.strftime('%Y-%m-%d %H:%M:%S', x.published_parsed)
                           ]
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

def word_tokenaize(doc):
    """
    Mecabを使用して与えられたテキストを解析する
    名詞のみを取り出してリストに格納する
    """
    try:
        tagger = MeCab.Tagger(" -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
        tagger.parse("")
        node = tagger.parse(doc)
        results = []
        lines=[]
        lines=node.split('\n')
        for item in lines:
           cw = item.split('\t')[0]
           if len(item) > 5:
              ps = item.split('\t')[1].split(',')[0]
              if  ps == '名詞':
                  results.append(cw)
        return results
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def getfeedword(input_file):
    """
    RSSフィードを保存したファイルからタイトルと説明文を取得する。
    """
    try:
        o = []
        with open(input_file, newline = "") as f:
             df = json.load(f)
             for i in range(len(df)):
                 for j in range(len(df[i])):
                     if df[i] is not None or type(df[i]) is not 'NoneType':
                        t = df[i][j]['title']
                        s = re.sub('<.*?>', "", df[i][j]['description'])
                        o +=[t,s]
             return o
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def main():
    """
    主処理
    第1引数で入力ファイルを取得し、名詞を抽出してランキングにする。
    meCabで処理した名詞の中から数値のものを除外する。
    """
    try:
        start_t = time.perf_counter()
#        input_file = sys.argv[1]

        feedurls = 'https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=JP'
        r = gtrend_get(feedurls)
        print(r)

#        feedword = getfeedword(input_file)
#        wl = 3
#        word = []
#        p = re.compile('^[0-9]+$')
#        for l in feedword:
#            wc = word_tokenaize(l)
#            o = [i for i in wc if not re.match(p,i)]
#            word.extend(o)
#        result = collections.Counter(word)
#        for word, cnt in sorted(result.items(),key=lambda x: x[1], reverse=True):
#            if len(word) > wl:
#               print(word, cnt)

        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
