import json
from requests_oauthlib import OAuth1Session
import pprint
import sys
import traceback
import yaml



def gettwitter_param():
    """
    ymlファイルから設定情報を取得する。
    """
    try:    
        with open('../config/config.yml', 'r') as yml:
             config = yaml.load(yml)
             consumer_key = config['twitter']['consumer_key']
             consumer_secret = config['twitter']['consumer_secret']
             token = config['twitter']['token']
             token_secret = config['twitter']['token_secret']

             result = dict(ck=consumer_key,cs=consumer_secret, 
                           at=token,ats=token_secret) 
             return result
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def main():
    """
    主処理　twitterにつぶやいて結果表示 

    """
    try:
        tp = gettwitter_param()
        twitter = OAuth1Session(tp['ck'],tp['cs'],tp['at'],tp['ats'])
        get_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        post_url = "https://api.twitter.com/1.1/statuses/update.json"
        print("呟く内容は？")
        tweet = input('>> ')
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

if __name__ == '__main__':
   main()

