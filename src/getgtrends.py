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
import pandas as pd
from pandas import Series, DataFrame
from pytrends.request import TrendReq

import mecaboperate as mec

def search(arg, cond):
    """
    jsonを解析する
    """
    res =[]
    if cond(arg):
        res.append(arg.values())
    if isinstance(arg, list):
        for item in arg:
            res += search(item, cond)
    elif isinstance(arg, dict):
        for value in arg.values():
            res += search(value, cond)
    return res
def has_star_key(arg):
    if isinstance(arg, dict):
        return arg.keys() == {'top', 'rising'}
def get_star(arg):
    return search(arg, has_star_key)


def gtrend_getfeed(urls):
    """
    GoogleトレンドのRSSフィードを取得する。
    """
    try:
        results=[]
        keys = [
                 'title','ht_approx_traffic','published_parsed'
               ]
        feed = feedparser.parse(urls)
        for x in feed.entries:
            if x is not None:
               if hasattr(x, 'title') and \
                  hasattr(x, 'ht_approx_traffic') and \
                  hasattr(x, 'published_parsed'):
                  values = [
                             x.title,
                             x.ht_approx_traffic.replace('+','').replace(',',''),
                             time.strftime('%Y-%m-%d %H:%M:%S', x.published_parsed)
                           ]
                  o = dict(zip(keys,values))
                  results.append(o)
        if results:
           results = sorted(results, key=lambda x:x['ht_approx_traffic'],reverse=True)
           return results
        else:
            return
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def gtrend_getvalue(kw_list,output_file,timeframe):
    """
    ライブラリを使用してGoogleTrendsからデータを取得する。
    #pytrends ref https://pypi.org/project/pytrends/#interest-by-region
    """
    #ファイル出力
    def exportdata(trendsdata,output_file_name):
        #data = pd.DataFrame(trendsdata)
        #for td in trendsdata.values(): 
        #    o=td.values()
        #o = [i for i in trendsdata.values()]
        o = get_star(trendsdata)
        print(len(o))


        #with open(output_file_name,'w') as f:
        #  for ele in o.value:
        #      f.write(ele+'\n')
        #     f.write(o)
        #o.to_csv(output_file_name)
    try:
        pytrends = TrendReq(hl='ja-JP', tz=360)
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='JP', gprop='')
        #関連キーワード
        trendsdata = pytrends.related_queries()
        o = output_file +"_query.csv"
        f = exportdata(trendsdata,o)
        """#関連トピック
        trendsdata = pytrends.related_topics()
        o = output_file +"_topics.csv"
        f = exportdata(trendsdata,o)
        #地域別の関心
        trendsdata = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
        o = output_file +"_region.csv"
        f = exportdata(trendsdata,o)
        #時系列
        trendsdata = pytrends.interest_over_time()
        o = output_file +"_overtime.csv"
        f = exportdata(trendsdata,o)
        #注目キーワード
        #trendsword = pytrends.trending_searches(pn='united_states') #アメリカ
        trendsword = pytrends.trending_searches(pn='japan') #日本
        o = "trend_word.csv"
        f = exportdata(trendsword,o) """

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
                        s = df[i][j]['description']
                        o +=[t,s]
             return o
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def getnumwords(targetword):
    """
    単語数を数えて上位からソートする
    """
    try:
        tw = collections.Counter(targetword)
        results = []
        keys = ['word','word_count']
        for word, cnt in sorted(tw.items(),key=lambda x: x[1], reverse=True):
            values = [word,cnt]
            w = dict(zip(keys,values))
            if w:
               results.append(w)
        if results:
           return results
        else:
           return
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))


def main():
    """
    主処理
    
    """
    try:
        start_t = time.perf_counter()

        input_file = sys.argv[1]
        output_file = sys.argv[2]

        #trendsurls = 'https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=JP'
        #gw = gtrend_getfeed(trendsurls)
        #print(gw)

        kw = ["Java","Python","JavaScript"]
        #tframe='today 5-y'
        tframe='2018-01-01 2018-6-30'
        
        #GoogleTorends
        gtrend_getvalue(kw,output_file,tframe)

        feedword = getfeedword(input_file)
        wl = 3
        word = []
        p = re.compile('^[0-9]+$')
        for l in feedword:
            if len(l) > wl :
               wc = mec.word_tokenaize(l)
               o = [i for i in wc if not re.match(p,i)]
               word.extend(o)
        
        fw = getnumwords(word)
        #print(fw)


        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
