import urllib
import webbrowser

import requests
from requests_oauthlib import OAuth1


API_KEY = ''
SECRET_KEY = ''

request_url = 'https://www.hatena.ne.jp/oauth/initiate?scope=read_public%2Cread_private%2Cwrite_public%2Cwrite_private'
authorize_url = 'https://www.hatena.ne.jp/oauth/authorize'
access_token_url = 'https://www.hatena.ne.jp/oauth/token'
callback_uri = 'oob'


def oauth_requests():
    # Get request token
    auth = OAuth1(API_KEY, SECRET_KEY, callback_uri=callback_uri)
    r = requests.post(request_url, auth=auth)
    request_token = dict(urllib.parse.parse_qsl(r.text))

    # User Authorization
    print('%s?oauth_token=%s&perms=delete' % (authorize_url, 
        request_token['oauth_token']))
    oauth_verifier = input("Please input PIN code:")
    auth = OAuth1(
        API_KEY,
        SECRET_KEY,
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        verifier=oauth_verifier)
    r = requests.post(access_token_url, auth=auth)

    access_token = dict(urllib.parse.parse_qsl(r.text))
    return access_token

if __name__ == '__main__':
    print(oauth_requests())
