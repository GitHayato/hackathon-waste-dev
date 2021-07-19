"""
    一時間に一度実行して、削除を検知すする。

    仕様：
        Rubyから必要な引数を受け取る
        過去30日間の「積み上げ」ツイート(内容、日付)を取得
        それらをhash化する
        Rubyに返す
"""

from hashing.hashingBysha256 import hash_exe
from twitter_api.get_tweet import TwitterAPI
from typing import Tuple
import time
from datetime import datetime, timezone

import argparse
from argparse import ArgumentError


# ログ取得
import logging
logger = logging.getLogger(__name__)
# ログレベル設定
logger.setLevel(logging.INFO)
##ハンドラ取得
get_handler = logging.FileHandler('app/controllers/concerns/hackason/logfile/exe_per_hour_cron.log')
logger.addHandler(get_handler)


def main(user_id:str, hash_value:str, start:str, end:str, count:int) -> Tuple:

    # スクリプトを実行毎に1足していく
    count_updated = count + 1

    # 今までの「積み上げ」ツイート(内容、日付)を取得
    twitter_api = TwitterAPI()
    now_time = time.time()


    # id = "HayatoProgram"
    tweets = twitter_api.regularly_get_user_tweets(user_id, start, now_time)

    # 前回のツイートを抽出
    pre_tweets = [(str(tweet.text), str(tweet.created_at.timestamp())) for tweet in tweets if (float(tweet.created_at.timestamp()) >= float(start)) & (float(tweet.created_at.timestamp()) <= float(end))]
    
    # 過去に一度も積み上げツイートがツイートされてないとき実行
    if not pre_tweets:

        # emptyをhash化する
        sha256_value = hash_exe("empty")

        if hash_value == sha256_value:
            # print("問題なし")
            count_updated = 0
            hasten_message = f'月に代わってお仕置きよ 早く積み上げツイートをしなさい！\n{datetime.fromtimestamp(now_time)}'
            twitter_api.send_directMessage(user_id, hasten_message)

        # hash値に問題があったとき：何もしない
        else:
            # print("hash値に問題あり！！！")
            pass

    else:
        sum_pre_tweet = ""
        # list内のツイートを連結する
        for tweet in pre_tweets:
            sum_pre_tweet += tweet[0] + tweet[1]
        
        # それらをhash化する
        prevalid_hash_value =  hash_exe(sum_pre_tweet)

        # hash値が異なるとき,お仕置きツイート
        if hash_value != prevalid_hash_value:
            post_message = f"#お仕置き執行　\n 改ざんを検知したわ。\n月に代わってお仕置きよ❤ @{user_id} \n{datetime.fromtimestamp(now_time)} "
            twitter_api.post_tweet(post_message)

        # ツイートしていない期間を計算。
        latest_tweet = float(tweets[0].created_at.timestamp())
        dif_time = twitter_api.clu_between_tweets_period(now_time, latest_tweet)

        # 二日間ツイートされてない時,催促DMを送る
        if twitter_api.jud_kotsukotsu_load(dif_time, period=2):
            count_updated = 0
            hasten_message = f'月に代わってお仕置きよ ついーとしなさい！ \n{datetime.fromtimestamp(now_time)}'
            twitter_api.send_directMessage(user_id, hasten_message)

        # 続いている場合は、応援DM
        else:
            # 1日に一回お祝いツイートをする
            if count_updated >= 24:
                count_updated = 0
                celebration_message = f'すごいわ！ これからも頑張って☆彡 \n{datetime.fromtimestamp(now_time)}'
                twitter_api.send_directMessage(user_id, celebration_message)


    # hash値,start,endの更新をしてrubyに返す。
    start_updated = now_time - (86400 * 30)
    end_updated = now_time

    # 今回ツイートを抽出
    now_tweets = [(str(tweet.text), str(tweet.created_at.timestamp())) for tweet in tweets if (float(tweet.created_at.timestamp()) >= start_updated) & (float(tweet.created_at.timestamp()) <= end_updated)]

    # 今回も積み上げツイートがツイートされてないとき実行
    if not now_tweets:

        # emptyをhash化する
        hash_value_updated = hash_exe("empty")
    
    else:
        sum_now_tweet = ""
        # list内のツイートを連結する
        for tweet in now_tweets:
            sum_now_tweet += (tweet[0] + tweet[1])
        
        # それらをhash化する
        hash_value_updated =  hash_exe(sum_now_tweet)
    
    logger.info(f'user_id:{user_id} | hash_value:{hash_value} | start:{datetime.fromtimestamp(float(start))} | end:{datetime.fromtimestamp(float(end))} | hash_value_updated:{hash_value_updated} | start_updated:{datetime.fromtimestamp(float(start_updated))} | end_updated:{datetime.fromtimestamp(float(end_updated))}')

    return  hash_value_updated, start_updated, end_updated, count_updated
    

# 実行ファイル指定後の引数を取得する。
def extra_argments() -> Tuple:
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--id')
    parser.add_argument('-hv', '--hashValue')
    parser.add_argument('-s', '--start')
    parser.add_argument('-e', '--end')
    parser.add_argument('-c', '--count')
    args = parser.parse_args()

    if (not args.id) or (not args.hashValue)or (not args.start) or (not args.end) or (not args.count):
        raise ArgumentError(None, '要素がありません')

    return (args.id, args.hashValue, args.start, args.end, args.count)


def get_hash_value(user_id, start, end):
    twitter_api = TwitterAPI()

    tweets = twitter_api.test_get_user_tweets(user_id, start, end)

    sum_tweet = ""
    # list内のツイートを連結する
    for tweet in tweets:
        sum_tweet += (tweet[0] + tweet[1])
    
    # それらをhash化する
    hash_value =  hash_exe(sum_tweet)

    return hash_value


if __name__ == "__main__":
    
    # mainを実行
    user_id, hash_value, start, end, count =  extra_argments()
    hash_value_updated, start_updated, end_updated, count_updated = main(user_id, hash_value, start, end, int(count))
    
    # Rubyにhash値を返す
    print(hash_value_updated, start_updated, end_updated, count_updated)

