import os
import re
import sys
import time
import traceback

import emoji
import neologdn

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
        s = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in s])
        return s
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))


def main():
    """
    主処理
    第1引数で指定されたディレクトリ配下のファイルをすべて処理する。

    """
    try:
        start_t = time.perf_counter()

        rootdir = sys.argv[1]

        i=0
        for root, dirs, files in os.walk(rootdir):
            i +=1
        j = 0
        for root, dirs, files in os.walk(rootdir):
            if j > 0:
               print('処理ディレクトリ{0}/{1}'.format(j,i-1))
               file_count = len(files)
               print('処理対象ファイル数{0}'.format(file_count))
            j +=1
            for file_ in files:
                input_file = os.path.join(root, file_)
                with open(input_file,'r') as inf:
                     s =inf.read()
                     o = strnormaraizer(s)
                with open(input_file,'w') as outf:
                     outf.write(o)

        end_t = time.perf_counter()

        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
