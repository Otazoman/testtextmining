import re
import sys
import traceback
import emoji
import neologdn

def strnormaraizer(str):
    """
    日本語を正規化する
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

#if __name__ == '__main__':
