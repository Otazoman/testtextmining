#!/usr/bin/env python3
# coding: utf-8
import csv
import collections
from operator import itemgetter
import sys
import time
import traceback

import MeCab
import japanesenormaraizer as jn

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

def main():
    """
    主処理
    第1引数から入力ファイル、第2引数から出力ファイルを取得する
    word_tokenaizeで解析した単語数を降順で並べ替えて出力する。
    """
    try:
        start_t = time.perf_counter()
        o = []
        r = []
        csvlist = []
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        for line in open(input_file, 'r'):
            line = jn.strnormaraizer(line)
            r = word_tokenaize(line)
            o.extend(r)
        result = collections.Counter(o)
        f = open(output_file + '.csv', 'w')
        writer = csv.writer(f, lineterminator='\n')
        for word, cnt in sorted(result.items(),key=lambda x: x[1], reverse=True):
            writer.writerow([word,cnt])
            print(word, cnt)
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
