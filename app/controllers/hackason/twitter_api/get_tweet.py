from typing import List, Tuple
import re
from datetime import datetime

import tweepy


class TwitterAPI:
    # 認証に必要なキーとトークン
    API_KEY = 'VkGXNeUcN0uNjzSgexc7kLH1J'
    API_SECRET = 'FYzMThkiatiObTiTcLdkRPKNfxJJSagNlhhrC5AQ9KufHSFdF7'
    ACCESS_TOKEN = '1403610869028642818-zotBriynYYCKeM9oqUG7hUmyuCpIOV'
    ACCESS_TOKEN_SECRET = 'ml3biVNmSpD636eF3pzQiS5yrrdgJi65DoNyTGu1rinlL'

    # APIの認証
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    # APIオブジェクトの作成
    api = tweepy.API(auth)


    """
        特定のユーザーの特定のツイートを取得する

        return 
               ツイート内容とツイートされた時間
    """
    def get_user_tweets(self, id:str) -> List[Tuple[str, datetime]]:
        # (1)リツイート、リプライのツイートは無視する。(2)「#今日の積み上げ」ツイートを抽出する
        tweets = [tweet for tweet in tweepy.Cursor(TwitterAPI.api.user_timeline, id=id).items(30) if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@') & (re.search("#今日の積み上げ", str(tweet.text)) != None)]

        # 各ツイートの内容と日付をlistに格納
        tweet_info = []
        for tweet in tweets:
            # print(tweet.text)
            # print(tweet.created_at)
            tweet_info.append((tweet.text, tweet.created_at))
        
        return tweet_info


    """
        tweet間の期間を計算

        return 
               二つのツイートされた時間の差
    """
    def clu_between_tweets_period(self, created_time1:datetime, created_time2:datetime) -> float:
        # unixtimeに変換する
        unix_time1 = created_time1.timestamp()
        unix_time2 = created_time2.timestamp()
        
        # 時間差を計算する
        dif_time = unix_time2 - unix_time1

        return dif_time


    """
        指定期間内に積み上げツイートをしているか判定する.

        return 
               積み上げツイートをしてるなら　　　 ->   True
               積み上げツイートをしていないなら　 ->   False 

    """
    def jud_kotsukotsu_load(self, dif_time:float, period:int):
        # 指定期間を秒に変換する。
        period_second = period * 86400

        if dif_time > period_second:
            return True
        
        return False



if __name__ == "__main__":

    twitter_api = TwitterAPI()
    
    # id = "kitiyama1152"
    id = "HayatoProgram"
    tweet_info = twitter_api.get_user_tweets(id)
    dif_time = twitter_api.clu_between_tweets_period(tweet_info[1][1], tweet_info[0][1])
    print(dif_time)
    