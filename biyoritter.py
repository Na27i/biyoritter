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

while 1:
    tweet = ""
    flag = 0

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
        #elif sent == "":
        #    mtl(1)
        #    flag = 1
        #    break
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
            print("   そのほかのコマンドなのん。いろんな機能があるん！")
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

    post_params = {"status" : tweet}
    post_res = twitter.post(post_url, params = post_params)

    if flag != 1:
        if post_res.status_code != 200:
            print("投稿に失敗したのんな～\n")
        else:
            print("投稿成功なのん！\n")