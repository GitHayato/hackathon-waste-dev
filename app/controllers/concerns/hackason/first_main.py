"""
    ユーザがアカウントの登録をした際、呼ばれるファイル

    仕様：
        Rubyから必要な引数を受け取る
        今までの「積み上げ」ツイート(内容、日付)を取得
        それらをhash化する
        Rubyに返す
"""

# import sys
# sys.path.append("hashing.py")

from hashing.hashingBysha256 import implement_hashing, hash_exe
from twitter_api.get_tweet import TwitterAPI
from datetime import datetime, date
from typing import Tuple


# 今日の日付のunixタイムを返す
def get_today_time() -> float:
    td_today = date.today().strftime('%s')
    return int(td_today)


# 昨日~31日間,一昨日~32日間のツイートを取得し、hash化する
def main(user_id:str) -> Tuple:

    # 今日の日付を求める
    td_today = get_today_time()

    # 昨日の日付が変わるギリギリの時間を求める
    yd_today = td_today - 2

    # # 一昨日の日付が変わるギリギリの時間を求める
    # dby_today = td_today - float(86400 * 1) - 2
    
    # 31日前の日付を求める
    ago_31days = yd_today - float(86400 * 30)
    # print(f'31 day ago: {datetime.fromtimestamp(ago_30days)}')

    # # 32日前の日付を求める
    # ago_32days = dby_today - float(86400 * 30)

    print(f'td_today: {datetime.fromtimestamp(td_today)}')
    print(f'yd_today: {datetime.fromtimestamp(yd_today)}')
    # print(f'dby_today: {datetime.fromtimestamp(dby_today)}')
    print(f'ago_31days: {datetime.fromtimestamp(ago_31days)}')
    # print(f'ago_32days: {datetime.fromtimestamp(ago_32days)}')

    # インスタンス化
    twitter_api = TwitterAPI()
    
    # 昨日~32日間の「積み上げ」ツイート(内容、日付)を取得する
    # id = "HayatoProgram"
    tweets_info = twitter_api.get_user_tweets(user_id, ago_31days, yd_today)
    print(f'tweets_info:{tweets_info}')
    print(f'len:{len(tweets_info)}')
    # tweets_info = twitter_api.get_user_tweets(user_id, ago_32days, yd_today)


    # # 昨日~31日間のツイートを一つの文字列にする。
    # yd_31_tweet_mix = ""
    # for tweet_info in tweets_info:
    #     if (float(tweet_info[1].timestamp()) >= ago_31days) & (float(tweet_info[1].timestamp()) <= yd_today):
    #         yd_31_tweet_mix += str(tweet_info[1].timestamp()) + str(tweet_info[0])

    # # それらをhash化する
    # yd_31_tweet_sha256 = hash_exe(yd_31_tweet_mix)
    # 昨日~31日間のツイートを一つの文字列にする。
    yd_31_tweet_mix = ""
    for tweet_info in tweets_info:        
        yd_31_tweet_mix += str(tweet_info[1].timestamp()) + str(tweet_info[0])

    # それらをhash化する
    yd_31_tweet_sha256 = hash_exe(yd_31_tweet_mix)


    # 一昨日~32日間のツイートを一つの文字列にする。
    # dby_32_tweet_mix = ""
    # for tweet_info in tweets_info:
    #     if (float(tweet_info[1].timestamp()) >= ago_32days) & (float(tweet_info[1].timestamp()) <= dby_today):
    #         dby_32_tweet_mix += str(tweet_info[1].timestamp()) + str(tweet_info[0])

    # # それらをhash化する
    # yd_32_tweet_sha256 = hash_exe(dby_32_tweet_mix)

    return yd_31_tweet_sha256
    
    # # それらをhash化する
    # pre_block = "96e7bd2465a8865989f806b8157ce89e9d94babf773a5eb2f7ef71250e89b6b4"
    # # pre_block = "test"
    # for i,info in enumerate(tweet_info):
    #     hash_valuse = implement_hashing(info[0], str(info[1]), pre_block)

    #     # 最後の要素の時実行
    #     if i == len(tweet_info) - 1:
    #         return hash_valuse

    #     # 前のブロック値を更新
    #     pre_block = hash_valuse
    

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id')
    args = parser.parse_args()
    user_id = args.id

    # mainを実行
    # yd_32_tweet_sha256, yd_31_tweet_sha256 = main(user_id)
    yd_31_tweet_sha256 = main(user_id)
    
    # Rubyにhash値を返す
    print(yd_31_tweet_sha256)
