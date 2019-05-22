import sys
import json
import re
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

# 置換コマンド
import cmd

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

# 線を引くだけ
def draw_line():
    for roop in range(10):
        print("- - - - - ", end="")
        if roop == 9:
            print("")

# TL表示
def mtl(count):
    get_params = {"count" : count}
    get_res = twitter.get(get_url, params = get_params)
    if get_res.status_code == 200:
        timelines = json.loads(get_res.text)
        draw_line()
        for get_tweet in timelines:
            print("  " + get_tweet['user']['name'])
            print(get_tweet['text'])
            print(get_tweet['created_at'] + "\n")
        draw_line()

# コマンドを表示
def cmd_disp():
    print("   置換コマンドなのん。入力するとウチが置換するのんな～")
    for i in range(cmd.cmd_len):
        print("   " + cmd.rep_cmd[i][0].ljust(3) + " : " + cmd.rep_cmd[i][1])
    print("\n   そのほかのコマンドなのん。隠し機能もあるん！")
    for i in range(cmd.oth_len):
        print("   " + cmd.oth_cmd[i][0].ljust(4) + " : " + cmd.oth_cmd[i][1])
    print("")

# ツイート本文の置換
def rep(sent):
    for i in range(cmd.cmd_len):
        if sent.find(cmd.rep_cmd[i][0]) != -1:
            sent = sent.replace(cmd.rep_cmd[i][0], cmd.rep_cmd[i][1])
    return sent

# ツイートの自動生成
def gen():
    tweetlist = ""
    cnt = 0
    get_params = {"count" : 1, "exclude_replies":True, "include_rts":False}
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
            print("ウチは暇じゃないのん……。")
    else :
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
            try:
                img = {"media" : open(sent[4:].replace('\n',''),'rb')}
                img_obj = twitter.post(upload_url, files = img)
                img_id = json.loads(img_obj.text)['media_id']
                break
            except FileNotFoundError:
                print("そんなファイルはないのんな〜")
                print("リトライするのん")
            except KeyError:
                print("アップロードに失敗したん……")
                print("リトライするのん")
                img_id = None

        elif sent == "":
            gen()
            flag = 1
            break
        elif sent == "cmd":
            cmd_disp()
            flag = 1
            break
        else:
            tweet += rep(sent)
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