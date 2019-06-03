import sys
import json
import re
import time
import calendar
import random
from janome.tokenizer import Tokenizer
from requests_oauthlib import OAuth1Session

# 置換コマンド
import cmd

# 認証情報
args = sys.argv
if len(args) == 1:
    import main as settings
else:
    import sub as settings

CK = settings.CONSUMER_KEY
CS = settings.CONSUMER_SECRET
AT = settings.ACCESS_TOKEN
ATS = settings.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

post_url = "https://api.twitter.com/1.1/statuses/update.json"
get_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
src_url = "https://api.twitter.com/1.1/search/tweets.json"
upload_url = "https://upload.twitter.com/1.1/media/upload.json"


# 線を引くだけ
def draw_line():
    for roop in range(10):
        print("- - - - - ", end="")
        if roop == 9:
            print("")


def time_cnv(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


# TL表示(検索)
def mtl(count, sent):
    if sent == None:
        get_params = {"count": count}
        get_res = twitter.get(get_url, params=get_params)
    else:
        sent += " exclude:retweets exclude:replies"
        get_params = {"q": sent, "count": count}
        get_res = twitter.get(src_url, params=get_params)

    if get_res.status_code == 200:
        timelines = json.loads(get_res.text)
        draw_line()
        if sent == None:
            for get_tweet in timelines:
                print("\n  " + get_tweet['user']['name'] + "   (@" +
                      get_tweet['user']['screen_name'] + ")")
                print(get_tweet['text'])
                print("\n" + "[ " + time_cnv(get_tweet['created_at']) + " ]\n")
                draw_line()
        else:
            for get_tweet in timelines["statuses"]:
                print("\n  " + get_tweet['user']['name'] + "   (@" +
                      get_tweet['user']['screen_name'] + ")")
                print(get_tweet['text'])
                print("\n" + "[ " + time_cnv(get_tweet['created_at']) + " ]\n")
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
    tweet = ""
    tweetlist = ""
    do = []
    get_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    get_params = {"count": 1, "exclude_replies": True, "include_rts": False}
    get_res = twitter.get(get_url, params=get_params)
    if get_res.status_code == 200:
        timelines = json.loads(get_res.text)
        #全ツイートを取得
        for i in timelines:
            tweet = (i["text"])
            tweet = tweet.split("http" , 1)[0]   #urlを削除
            tweet = tweet.split("@", 1)[0]  #usernameを削除
            tweet = tweet.split(" ")[0]   #半角スペースを削除
            tweet = tweet.split("　")[0]   #全角スペースを削除
            tweetlist += tweet

        post_url = "https://api.twitter.com/1.1/statuses/update.json"
        t = Tokenizer()
        tokens = t.tokenize(tweetlist)
        for token in tokens:
            partOfSpeech = token.part_of_speech.split(',')[0]
            if partOfSpeech == u"動詞":
                do.append(token.base_form)

        if len(do) == 0:
            post_params = {"status": "ウチは何もしたくない気分なん"}
            post_res = twitter.post(post_url, params=post_params)
        else :
            sent =  "ウチも" + do[random.randrange(len(do))] + "のん！"
            post_params = {"status": sent}
            post_res = twitter.post(post_url, params=post_params)

        if post_res.status_code != 200:
            print("二番煎じは面白くないのん……\n")
    else:
        print("ツイートの生成に失敗したのんな～\n")
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
        elif sent == "ers":
            print("入力した文字列を消去したのん！\n")
            flag = 1
            break
        elif sent == "src":
            src_word = input(">> ")
            mtl(25, src_word)
            flag = 1
            break
        elif sent == "mtl":
            mtl(25, None)
            flag = 1
            break
        elif sent.find("-mtl") != -1:
            try:
                input_params = int(input(">> "))
            except:
                input_params = int(25)

            if int(input_params) > 200:
                mtl(200, None)
            else:
                mtl(input_params, None)
            flag = 1
            break
        elif re.match(img_reg, sent):
            try:
                img = {"media": open(sent[4:].replace('\n', ''), 'rb')}
                img_obj = twitter.post(upload_url, files=img)
                img_id = json.loads(img_obj.text)['media_id']
                break
            except FileNotFoundError:
                print("そんなファイルはないのんな〜")
                print("リトライするのん！\n")
            except KeyError:
                print("アップロードに失敗したん……")
                print("リトライするのん！\n")
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
            tweet += "\n"

    if flag == 1:
        tweet = ""
    elif flag != 1:
        if img_id:
            post_params = {"status": tweet, "media_ids": [img_id]}
        else:
            post_params = {"status": tweet}
        post_res = twitter.post(post_url, params=post_params)

        if post_res.status_code != 200:
            print("投稿に失敗したのんな～\n")
        else:
            print("投稿成功なのん！\n")