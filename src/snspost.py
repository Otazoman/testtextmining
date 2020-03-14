# coding: utf-8
from apiclient.discovery import build
import argparse
import httplib2
import json
import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
import os
import pprint
import sys
import time
import traceback
import yaml

from oauth2client.client import OAuth2WebServerFlow
from oauth2client        import tools,file


def get_authkey(snsname):
    """
    ymlファイルから設定情報を取得する。
    """
    try:    
        with open('../config/sns_config.yml', 'r') as yml:
             config = yaml.safe_load(yml)
             if snsname == 'blogger':
                client_id     = config[snsname]['client_id']
                client_secret = config[snsname]['client_secret']
                scope         = config[snsname]['scope']
                redirect_uri  = config[snsname]['redirect_uri']
                post_blog_id  = config[snsname]['post_blog_id']
                result = dict(
                                ci=client_id,cs=client_secret, 
                                sc=scope,ru=redirect_uri,pb=post_blog_id
                         )
             else:
                 consumer_key = config[snsname]['consumer_key']
                 consumer_secret = config[snsname]['consumer_secret']
                 token = config[snsname]['token']
                 token_secret = config[snsname]['token_secret']
                 result = dict(
                                ck=consumer_key,cs=consumer_secret,
                                at=token,ats=token_secret
                          ) 
             return result
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def post_blogger(postcontent):
    """
    Bloggerに投稿

    """
    try:
        ta = get_authkey('blogger')
        flow = OAuth2WebServerFlow(client_id=ta['ci'],
                                    client_secret=ta['cs'],
                                    scope=ta['sc'],
                                    redirect_uri=ta['ru'])
        storage = file.Storage('credentials.dat')
        credentials = storage.get()
        blogid = ta['pb']

        if credentials is None or credentials.invalid:
           credentials = tools.run_flow(flow, storage)
        
        http = credentials.authorize(http = httplib2.Http())
        service = build('blogger', 'v3', http=http)
        posts = service.posts()

        body = {
                  "kind": "blogger#post",
                  "id": blogid,
                  "title": "POSTED_" + postcontent,
                  "content": postcontent
              }
        insert = posts.insert(blogId=blogid, body=body)
        posts_doc = insert.execute()
        
        if posts_doc['status'] == 'LIVE':
            print('SUCCESS')
        else:
            print("ERROR : %d" % post_doc)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def post_twitter(postcontent):
    """
    twitterに投稿

    """
    try:
        ta = get_authkey('twitter')
        twitter = OAuth1Session(ta['ck'],ta['cs'],ta['at'],ta['ats'])
        get_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        post_url = "https://api.twitter.com/1.1/statuses/update.json"
        tweet = postcontent
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

def post_hatena(postword,url,tags):
    """
    はてなブックマークに追加
    """
    try:
        ta = get_authkey('hatena')
        auth = OAuth1(ta['ck'],ta['cs'],ta['at'],ta['ats'])
        bookmark_api_url = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"
        tagstr =""
        for t in tags:
            tagstr = tagstr + "&tags=" + t 
        req = requests.post( 
                bookmark_api_url + "?url=" + url + 
                "&comment=" + postword  +
                tagstr + 
                "&private=1",auth=auth
              )
        
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

def getpostdata(inputfile_name):
    """
    投稿用データ取得
    """
    try:
        #ファイルオープン
        with open(inputfile_name) as f:
             r = [e for inner_list in json.load(f) for e in inner_list]
             return r

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
        print('Please input inputfilename')
        input_file = input('>>')
        if not input_file:
           print("Please input inputfilename!!")
           sys.exit()
        json_data = getpostdata(input_file)
        cnt = 1
        for s in json_data:
            ohtml = """
            <div id = content>
                <div id ='name'>
                   取得元：{0}
                </div>
                <div id ='name'>
                   取得元：{1}
                </div>
                <div id ='title'>
                   記事タイトル:{1}
                </div>
                <a href ="{2}">記事リンク</a>
                <div id ='updateddate'>
                   更新日時:{3}
                </div>
            </div>
            """
            content = ohtml.format(s['category'], s['name'], s['title'], s['link'], s['updated'])
            comment = 'テスト' + str(cnt)
            tags=[]
            tags.append(s['category'])
            bookmark_url = s['link']
            time.sleep(1)
            #post_hatena(comment,bookmark_url,tags)
            #post_blogger(content)
            post_twitter(comment)
            #print(s['description'])
            cnt +=1
        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))        

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()

