"""
    ユーザがアカウントの登録をした際、呼ばれるファイル

    仕様：
        Rubyから必要な引数を受け取る
        今までの「積み上げ」ツイート(内容、日付)を取得
        それらをhash化する
        Rubyに4つの値を返す -> hash値、start時間、end時間、count数　
"""


from hashing.hashingBysha256 import implement_hashing, hash_exe
from twitter_api.get_tweet import TwitterAPI
from datetime import datetime, date
import time
from typing import Tuple


# 今日の日付のunixタイムを返す
def get_today_time() -> float:
    td_today = date.today().strftime('%s')
    return int(td_today)


# 昨日~31日間,一昨日~32日間のツイートを取得し、hash化する
def main(user_id:str) -> Tuple:

    # 今日の日付を求める
    now_time = time.time()

    # 昨日の日付が変わるギリギリの時間を求める
    # yd_today = td_today - 2

    # # 一昨日の日付が変わるギリギリの時間を求める
    
    # 31日前の日付を求める
    # ago_31days = yd_today - float(86400 * 30)
    ago_30days = now_time - float(86400 * 30)
    
    # インスタンス化
    twitter_api = TwitterAPI()
    
    # 昨日~32日間の「積み上げ」ツイート(内容、日付)を取得する
    tweets_info = twitter_api.get_user_tweets(user_id, ago_30days, now_time)
    
    # 昨日~31日間のツイートを一つの文字列にする。
    yd_30_tweet_mix = ""
    for tweet_info in tweets_info:        
        yd_30_tweet_mix += str(tweet_info[0]+ str(tweet_info[1].timestamp()))

    # それらをhash化する
    yd_30_tweet_sha256 = hash_exe(yd_30_tweet_mix)

    start = ago_30days
    end  = now_time

    return yd_30_tweet_sha256, start, end
        

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id')
    args = parser.parse_args()
    user_id = str(args.id)

    # mainを実行
    yd_30_tweet_sha256, start, end = main(user_id)

    count = 0
    
    # Rubyにhash値を返す
    print(yd_30_tweet_sha256, start, end, count)
