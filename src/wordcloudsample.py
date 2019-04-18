import collections
import csv
from operator import itemgetter
import requests
import sys
import traceback

import matplotlib.pyplot as plt
import MeCab
from wordcloud import WordCloud

def create_wordcloud(txt,out_file):
    """
    テキストを受取ってWordCloudを生成する。
    """
    try:
        # フォントパス指定。
        fpath = "/usr/share/fonts/opentype/ipaexfont-mincho/ipaexm.ttf"
        # ストップワード
        stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u' こと', u'これ', u'さん', u'して', \
                 u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',  \
                 u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で', \
                 u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']
        wordcloud = WordCloud(background_color="white",font_path=fpath, width=900, height=500, \
                              stopwords=set(stop_words)).generate(txt)
        wordcloud.to_file(out_file+'.png')
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

def main():
    """
    主処理
    第1引数から入力ファイル、第2引数から出力ファイルを取得する
    word_tokenaizeで解析した単語の解析結果を加工する。
    加工データは単語数を降順でソートしたCSVとWordCloudのpngファイルとして出力さ れる。
    """
    try:
        o = []
        r = []
        csvlist = []
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print('operation start')
        for line in open(input_file, 'r'):
            r = word_tokenaize(line)
            o.extend(r)
        result = collections.Counter(o)
        create_wordcloud(' '.join(o),output_file)

        f = open(output_file + '.csv', 'w')
        writer = csv.writer(f, lineterminator='\n')
        for word, cnt in sorted(result.items(),key=lambda x: x[1], reverse=True):
            writer.writerow([word,cnt])
        f.close
        print('operation end')
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()

