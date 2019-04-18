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


def gtrend_get():
    """
    Googleトレンドのデータを取得する。
    """
    try:
        pytrend = TrendReq()

        trending_searches_df = pytrend.trending_searches(pn='p4')
        print(trending_searches_df["title"])

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
    """
    try:
        start_t = time.perf_counter()
        input_file = sys.argv[1]

        feedword = getfeedword(input_file)

        word = []
        for l in feedword:
            wc = word_tokenaize(l)
            word.extend(wc)

        result = collections.Counter(word)
        for word, cnt in sorted(result.items(),key=lambda x: x[1], reverse=True):
            print(f"{word} : {cnt}")

        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
