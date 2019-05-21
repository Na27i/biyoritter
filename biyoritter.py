import sys
import json
import re
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

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

post_url = "https://api.twitter.com/1.1/statuses/update.json"
get_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
upload_url = "https://upload.twitter.com/1.1/media/upload.json"

def mtl(count):
    get_params = {"count" : count}
    get_res = twitter.get(get_url, params = get_params)
    if get_res.status_code == 200:
        timelines = json.loads(get_res.text)
        for roop in range(10):
            print("- - - - - ", end="")
            if roop == 9:
                print("")
        for get_tweet in timelines:
            print("  " + get_tweet['user']['name'])
            print(get_tweet['text'] + "\n")
        for roop in range(10):
            print("- - - - - ", end="")
            if roop == 9:
                print("")

def gen():
    tweetlist = ""
    cnt = 0
    get_params = {"count" : 1, 'exclude_replies':True, 'include_rts':False,}
    get_res = twitter.get(get_url, params = get_params)
    if get_res.status_code == 200:
        timelines = json.loads(get_res.text)
        for roop in timelines:
            tweetlist = (roop["text"])
        a = Analyzer(token_filters=[POSKeepFilter(['動詞'])])
        for token in a.analyze(tweetlist):
            cnt += 1
        
        if cnt == 0:
            post_params = {"status" : "ウチは何もしたくない気分なのん。"}
            post_res = twitter.post(post_url, params = post_params)
        elif cnt == 1:
            post_params = {"status" : "ウチも" + token.base_form + "のん！"}
            post_res = twitter.post(post_url, params = post_params)
        else:
            post_params = {"status" : "ウチにはやることがいっぱいなのん……。"}
            post_res = twitter.post(post_url, params = post_params)

        if post_res.status_code != 200:
            print("なにかがおかしいのん……。")
    print("")

while 1:
    tweet = ""
    flag = 0
    img_reg = r'img:.+'
    img_id = None

    print("ツイート本文を入力するのんな～")
    print("困ったら cmd を入力するのん！ウチが助けるのん！")

    while 1:
        sent = input(">> ")
        if sent == "exit":
            exit(0)
        elif sent == "sub":
            break
        elif sent == "mtl":
            mtl(25)
            flag = 1
            break
        elif sent.find("-mtl") != -1:
            try:
                input_params = int(input(">> "))
            except:
                input_params = int(25)
            
            if int(input_params) > 200:
                mtl(200)
            else:
                mtl(input_params)
            flag = 1
            break
        elif re.match(img_reg, sent):
            img = {"media" : open(sent[4:].replace('\n',''),'rb')}
            img_obj = twitter.post(upload_url, files = img)
            img_id = json.loads(img_obj.text)['media_id']
            break
        elif sent == "":
            gen()
            flag = 1
            break
        elif sent == "cmd":
            print("   置換コマンドなのん。入力するとウチが置換するのんな～")
            print("   -ps  : ヽ(廿Δ廿 )にゃんぱすー")
            print("   -u   : ウチ")
            print("   -na  : なん")
            print("   -no  : のん")
            print("   -ru  : るん")
            print("   -ta  : たん")
            print("   -ao  : なのん")
            print("   -on  : のんな～\n")
            print("   そのほかのコマンドなのん。隠し機能もあるん！")
            print("   sub  : 入力した文字列をツイートするのん！")
            print("   mtl  : 自分のツイートを表示するのんな～。")
            print("   -mtl : 打った後に任意の数を入力するのん。ウチがその数だけツイートを表示させるのん！")
            print("   exit : プログラムを終了させるのん。\n")
            flag = 1
            break
        else:
            if sent.find("-ps") != -1:
                sent = sent.replace("-ps", "ヽ(廿Δ廿 )にゃんぱすー")
            if sent.find("-u") != -1:
                sent = sent.replace("-u" , "ウチ")
            if sent.find("-na") != -1:
                sent = sent.replace("-na", "なん")
            if sent.find("-no") != -1:
                sent = sent.replace("-no", "のん")
            if sent.find("-ru") != -1:
                sent = sent.replace("-ru", "るん")
            if sent.find("-ta") != -1:
                sent = sent.replace("-ta", "たん")
            if sent.find("-ao") != -1:
                sent = sent.replace("-ao", "なのん")
            if sent.find("-on") != -1:
                sent = sent.replace("-on", "のんな～")
            tweet += sent
            tweet += '\n'

    if img_id:
        post_params = {"status" : tweet, "media_ids":[img_id]}
    else:
        post_params = {"status" : tweet}
    post_res = twitter.post(post_url, params = post_params)

    if flag != 1:
        if post_res.status_code != 200:
            print("投稿に失敗したのんな～\n")
        else:
            print("投稿成功なのん！\n")