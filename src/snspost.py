import json
import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
import pprint
import sys
import traceback
import yaml



def get_authkey(snsname):
    """
    ymlファイルから設定情報を取得する。
    """
    try:    
        with open('../config/config.yml', 'r') as yml:
             config = yaml.load(yml)
             consumer_key = config[snsname]['consumer_key']
             consumer_secret = config[snsname]['consumer_secret']
             token = config[snsname]['token']
             token_secret = config[snsname]['token_secret']

             result = dict(ck=consumer_key,cs=consumer_secret, 
                           at=token,ats=token_secret) 
             return result
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def post_twitter(postword):
    """
    twitterに投稿

    """
    try:
        ta = get_authkey('twitter')
        twitter = OAuth1Session(ta['ck'],ta['cs'],ta['at'],ta['ats'])
        get_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        post_url = "https://api.twitter.com/1.1/statuses/update.json"
        tweet = postword
        print('-------------------------------')
        params = {"status" : tweet}
        req = twitter.post(post_url, params = params)
        if req.status_code == 200:
           params ={'count' : 1}
           rreq = twitter.get(get_url, params = params)
           if rreq.status_code == 200:
              timeline = json.loads(rreq.text)
              for tweet in timeline:
                  print(tweet['user']['name']+'::'+tweet['text'])
                  print(tweet['created_at'])
                  print('----------------------------------------------------')
        else:
           print("ERROR : %d" % req.status_code)
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))


def post_hatena(postword):
    """
    はてなブックマークに追加
    """
    try:
        ta = get_authkey('hatena')
        #pprint.pprint(ta) 

        auth = OAuth1(ta['ck'],ta['cs'],ta['at'],ta['ats'])

        pprint.pprint(auth)


        bookmark_api_url = "http://api.b.hatena.ne.jp/1/my/bookmark"
        bookmark_url = "https://tohonokai.com"
        
        req = requests.post(bookmark_api_url + "?url=" + bookmark_url, 
                auth=auth)
        
        if req.status_code == 200:
           print('SUCCESS')
        else:
           print("ERROR : %d" % req.status_code)
           print(req.headers)
           print(req.text)


    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))


def main():
    """
    主処理　twitterにつぶやいて結果表示 

    """
    try:
        print("呟く内容は？")
        content = input('>> ')
        #post_twitter(content)
        post_hatena(content)
    
    
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()

