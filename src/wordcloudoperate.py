import sys
import traceback
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
                 u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'',u'0',u'こと',u'ん']
        wordcloud = WordCloud(background_color="white",font_path=fpath, width=900, height=500, \
                              stopwords=set(stop_words)).generate(txt)
        wordcloud.to_file(out_file+'.png')
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
