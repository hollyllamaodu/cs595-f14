# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "QX9UsnHmngd6vD20LgEBXtvoN"
CONSUMER_SECRET = "Kkvt4i7x2pglyl8qhSlzdoHc2vjexNlrW8xGNZZeaFY2QjavQx"

OAUTH_TOKEN = "2825370151-dNfwsYgzC12FUyZjM4MhoXu4D7hMmG1RguUd3q0"
OAUTH_TOKEN_SECRET = "pZV2GtrPOPG9v3V0ugTWYqgm0KpyKrGlFQTj5djQu5I8C"

##Save Result to File
file1 = open('twitterFriends.txt','w')

def setup_oauth():
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r=requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    
    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]
    
    ##Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url
    
    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)
                   
    ##Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]
                   
    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=OAUTH_TOKEN,
                   resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
        oauth = get_oauth()
        r=requests.get(url="https://api.twitter.com/1.1/friends/list.json?cursor=-1&screen_name=phonedude_mln&skip_status=true&include_user_entities=false&count=200", auth=oauth)
        p=r.json()["users"]
        file1.write("Screen_Name, Number_Friends")
        file1.write("\n")

        for f in p:
            name=f["screen_name"]
            count=f["friends_count"]
            file1.write(name + "," + str(count) + "\n")

file1.close()