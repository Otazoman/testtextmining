#!/usr/bin/env python3
# coding: utf-8
import os
from flask import Flask, request, redirect, session
from furl import furl
from requests_oauthlib import OAuth1Session

app = Flask(__name__)
# xxxxxには、取得したランダムなシークレットキーを入力する。
app.secret_key = b""

OAUTH_CONSUMER_KEY = ''
OAUTH_CONSUMER_SECRET = ''

TEMPORARY_CREDENTIAL_REQUEST_URL = 'https://www.hatena.com/oauth/initiate'
RESOURCE_OWNER_AUTHORIZATION_URL = 'https://www.hatena.ne.jp/oauth/authorize'
TOKEN_REQUEST_URL = 'https://www.hatena.com/oauth/token'

CALLBACK_URI = 'http://127.0.0.1:5000/callback_page'
SCOPE = {'scope': 'read_public,write_public'}

@app.route('/')
def index():
    oauth = OAuth1Session(OAUTH_CONSUMER_KEY, client_secret=OAUTH_CONSUMER_SECRET, callback_uri=CALLBACK_URI)
    fetch_response = oauth.fetch_request_token(TEMPORARY_CREDENTIAL_REQUEST_URL, data=SCOPE)

    session['request_token'] = fetch_response.get('oauth_token')
    session['request_token_secret'] = fetch_response.get('oauth_token_secret')

    redirect_url = furl(RESOURCE_OWNER_AUTHORIZATION_URL)
    redirect_url.args['oauth_token'] = session['request_token']
    return redirect(redirect_url.url)

@app.route('/callback_page')
def callback_page():
    verifier = request.args.get('oauth_verifier')
    oauth = OAuth1Session(OAUTH_CONSUMER_KEY,
                          client_secret=OAUTH_CONSUMER_SECRET,
                          resource_owner_key=session['request_token'],
                          resource_owner_secret=session['request_token_secret'],
                          verifier=verifier)

    access_tokens = oauth.fetch_access_token(TOKEN_REQUEST_URL)
    access_token = access_tokens.get('oatuh_token')
    access_secret = access_tokens.get('oauth_token_secret')
    return "access_token: {}, access_token_secret: {}".format(access_token, access_secret)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
