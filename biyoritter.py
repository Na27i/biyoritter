import sys
import json

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

get_params = {
    "count" : 1,
    "exclude_replies" :True,
    "include_rts":False
    }

while 1:
    tweet = ''
    flag = 0

    print("ツイート本文を入力するのんな～")
    print("困ったら コマンド か cmd を入力するのん！ウチが助けるのん！")

    while 1:
        sent = input('>> ')
        if sent == "quit" or sent == "exit":
            exit(0)
        elif sent == "sub":
            break
        elif sent == "":
            get_res = twitter.get(get_url, params = get_params)
            if get_res.status_code == 200:
                timelines = json.loads(get_res.text)
                for get_tweet in timelines:
                    print(get_tweet['text'])
            flag = 1
            break
        elif sent == "cmd" or sent == "コマンド":
            print("   下のコマンドを入力するとウチが置換するのんな～")
            print("   -ps  : ヽ(廿Δ廿 )にゃんぱすー")
            print("   -u   : ウチ")
            print("   -na  : なん")
            print("   -no  : のん")
            print("   -ru  : るん")
            print("   -ta  : たん")
            print("   -ao  : なのん")
            print("   -on  : のんな～\n")
            print("   本文入力後に sub って打つとツイートするのん！")
            print("   exit か quit って打つとプログラムが終了するのんな～\n")
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

    post_params = {"status" : tweet}
    post_res = twitter.post(post_url, params = post_params)

    if flag != 1:
        if post_res.status_code != 200:
            print("投稿に失敗したのんな～\n")
        else:
            print("投稿成功なのん！\n")