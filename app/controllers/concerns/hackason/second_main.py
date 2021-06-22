"""
    ユーザがアカウントの登録をした際、呼ばれるファイル

    仕様：
        Rubyから引数として、「ID」、「hash値」を受け取る
        昨日までの「#積み上げ」ツイートを取得して、改ざんがないか検証する -> 改ざんがあれば公式ツイートから改ざんツイートを行う
        今日の「#積み上げ」ツイート(内容、日付)を取得しhash値を更新する
        Rubyに返す
"""

import argparse
from argparse import ArgumentError
from datetime import datetime, date
from typing import Tuple
from hashing.hashingBysha256 import hash_exe
from twitter_api.get_tweet import TwitterAPI


def get_today_time() -> int:
    td_today = date.today().strftime('%s')
    return int(td_today)


"""
    仕様：
        ➀積み上げツイートに改ざんがないチェック
            　あれば、公式ツイートから告知改ざんツイート、DMを送る
        ⓶hash値を更新する

    return -> 「アップデート後のhash値」と「前日のhash値」を返す

"""
def main(user_id:str, pre_hash_Value:str) -> Tuple:

    """
        使用する昨日～32日前のツイートを取得する
    """

    # 昨日のギリギリの日付を求める(23:59:58)
    yd = float(get_today_time() + 86400 - 2)

    # 一昨日のギリギリの日付を求める(23:59:58)
    dby = yd - 86400

    # 31日前の日付を求め
    ago_31days = yd - (86400 * 30)

    ago_32days = dby - (86400 * 30)
    
    # 昨日～31日,一昨日～32日分のツイートを抽出
    twitter_api = TwitterAPI()
    dby_32days_tweet_info, yd_31days_tweet_info = twitter_api.get_user_tweets_byTime(user_id, yd, dby, ago_31days, ago_32days)

    
    """
        一昨日の積み上げツイートに改ざんがないかチェックする。
    """

    # 一昨日~32日間のツイートを一つの文字列にする。
    dby_32_tweet_mix = ""
    for tweet_info in dby_32days_tweet_info:        
        dby_32_tweet_mix += str(tweet_info[1].timestamp()) + str(tweet_info[0])

    # それらをhash化する
    dby_32_tweet_sha256 = hash_exe(dby_32_tweet_mix)

    
    #　データベースに保存したhash値と比較する。
    if  dby_32_tweet_sha256 != dby_32_tweet_sha256:
        #  改ざんされた為、公式Twitterで改ざんされたツイートを行う。：hash値は今後改ざん後のモノを使う
        twitter_api.post_tweet(f"#お仕置き執行　\n 改ざんを検知したわ。\n月に代わってお仕置きよ❤ @{user_id}")
        
        # 催促メッセージ
        message_1 = f'月に代わってお仕置きよ ついーとしなさい！'
        twitter_api.send_directMessage(user_id, message_1)



    """
        昨日のツイートから新しいhash値を取得する
    """

    # 昨日~31日間のツイートを一つの文字列にする。
    yd_31_tweet_mix = ""
    for tweet_info in yd_31days_tweet_info:
        yd_31_tweet_mix += str(tweet_info[1].timestamp()) + str(tweet_info[0])

    # それらをhash化する
    yd_31_tweet_sha256 = hash_exe(yd_31_tweet_mix)

    return yd_31_tweet_sha256


# 実行ファイル指定後の引数を取得する。
def extra_argments() -> Tuple:
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--id')
    parser.add_argument('-phv', '--prehashValue')
    args = parser.parse_args()

    if (not args.id) or (not args.prehashValue):
        raise ArgumentError(None, '要素がありません')

    return (args.id, args.prehashValue)
            

if __name__ == "__main__":
    """
        ツイートを取得したstart:endの時間をdbから貰う必要がある。
    """

    # 実行ファイル指定後の引数を取得する
    user_id, pre_hash_Value = extra_argments()

    # mainを実行 -> 更新後のhash値とひとつ前のブロックのhash値を返す
    yd_31_tweet_sha256 = main(user_id, pre_hash_Value)
    
    # # Rubyにhash値を返す
    print(yd_31_tweet_sha256)
