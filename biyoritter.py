import json
import sys

args = sys.argv

if len(args) == 1 :
    import main as settings
else :
    import sub as settings

from requests_oauthlib import OAuth1Session

CK = settings.CONSUMER_KEY
CS = settings.CONSUMER_SECRET
AT = settings.ACCESS_TOKEN
ATS = settings.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/statuses/update.json"

while 1:
    tweet = ''
    fin = ''
    flag = 0
    
    print("ツイート本文を入力するのんな～")
    while 1:
        sent = input('>> ')
        if sent == "quit" or sent == "exit":
            exit(0)        	
        elif sent == "sub":
            break
        elif sent == "cmd":
            print("コマンドを入力するとウチが置換するのんな～")
            print("-ny : ヽ(廿Δ廿 )にゃんぱすー")
            print("-n  : なのん")
            print("-N  : のんな～")
            flag = 1
            break
        else:
        	if sent.find("-") != -1:
        		fin = sent.replace("-ny", "ヽ(廿Δ廿 )にゃんぱすー").replace("-n","なのん").replace("-N", "のんな～。")
        		tweet += fin
        	else:
        		tweet += sent
        	tweet += '\n'

    if flag == 0:
        params = {"status" : tweet}
        res = twitter.post(url, params = params)
        if res.status_code != 200:
            print("投稿に失敗したのんな～")