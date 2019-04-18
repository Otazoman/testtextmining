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

def main():
    """
    主処理
    第1引数から入力ファイル、第2引数から出力ファイルを取得する
    """
    try:
        start_t = time.perf_counter()
        input_file = sys.argv[1]

        t = []
        d = []

        with open(input_file, newline = "") as f:
             df = json.load(f)
             for i in range(len(df)):
                 for j in range(len(df[i])):
                     if df[i] is not None or type(df[i]) is not 'NoneType':
                        t.append(df[i][j]['title'])
                        s = re.sub('<.*?>', "", df[i][j]['description'])
                        #s = df[i][j]['description']
                        d.append(s)
             print(t)
             print(d)

        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
