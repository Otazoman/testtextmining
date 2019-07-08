#!/usr/bin/env python3
# coding: utf-8
import collections
import csv
from operator import itemgetter
import os
import requests
import sys
import time
import traceback

import japanesenormaraizer as jn
import mecaboperate as mec
import wordcloudoperate as wc


def main():
    """
    主処理
    mecabで解析した単語の解析結果を加工する。
    加工データは単語数を降順でソートしたCSVとWordCloudのpngファイルとして出力される。
    """
    try:
        start_t = time.perf_counter()
        o = []
        r = []
        csvlist = []

        print('Please input inputfilename')
        input_file = input('>>')
        if not input_file:
           print("Please input inputfilename!!")
           sys.exit()

        print('Please input outputfilename')
        output_file = input('>>')
        if not output_file:
           name,ext = os.path.splitext( os.path.basename(input_file) )
           output_file = name
           print('outputfilename auto generate {0}'.format(output_file))
        else:
            output_file = output_file

        print('operation start')
        for line in open(input_file, 'r'):
            line = jn.strnormaraizer(line)
            r = mec.word_tokenaize(line)
            o.extend(r)
        result = collections.Counter(o)
        wc.create_wordcloud(' '.join(o),output_file)

        f = open(output_file + '.csv', 'w')
        writer = csv.writer(f, lineterminator='\n')
        for word, cnt in sorted(result.items(),key=lambda x: x[1], reverse=True):
            writer.writerow([word,cnt])
        f.close

        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()