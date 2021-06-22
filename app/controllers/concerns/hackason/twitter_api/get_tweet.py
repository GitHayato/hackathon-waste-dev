from typing import List, Tuple
import re
from datetime import datetime
import os

import tweepy
from tweepy import api

from dotenv import load_dotenv


class TwitterAPI:
    # 認証に必要なキーとトークン

    load_dotenv()

    # 環境変数を参照
    API_KEY = os.getenv('OSHIOKI_API_KEY')
    API_SECRET = os.getenv('OSHIOKI_API_SECRET')
    ACCESS_TOKEN = os.getenv('OSHIOKI_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('OSHIOKI_ACCESS_TOKEN_SECRET')

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
    # first_main.pyで呼び出すメソッド
    def get_user_tweets(self, user_id:str, since:str, until:str) -> List[Tuple[str, datetime]]:

        # (1)リツイート、リプライのツイートは無視する。(2)「#今日の積み上げ」ツイートを抽出する
        tweets = [tweet for tweet in tweepy.Cursor(TwitterAPI.api.user_timeline, id=user_id).items(500) if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@') & (re.search("#今日の積み上げ", str(tweet.text)) != None) & (float(tweet.created_at.timestamp()) >= float(since)) & (float(tweet.created_at.timestamp()) <= float(until))]

        # 各ツイートの内容と日付をlistに格納
        tweet_info = []
        for tweet in tweets:
            # print(tweet.text)
            # print(tweet.created_at)
            tweet_info.append((tweet.text, tweet.created_at))
        
        return tweet_info

    # second_main.pyで呼び出すメソッド
    def get_user_tweets_byTime(self, user_id:str, yd:float, dby:float, ago_31days:float, ago_32days:float) -> Tuple:
        
        # (1)リツイート、リプライのツイートは無視する。(2)「#今日の積み上げ」ツイートを抽出する
        tweets = [tweet for tweet in tweepy.Cursor(TwitterAPI.api.user_timeline, id=user_id).items(limit=500) if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@') & (re.search("#今日の積み上げ", str(tweet.text)) != None)]

        # 昨日~31日前のツイートを抽出
        # for_31_1days_tweet = [tweet for tweet in tweets if (float(tweet.created_at.timestamp()) >= float(since)) & (float(tweet.created_at.timestamp()) <= float(latest_tweet_time))]
        yd_31days_tweet = [tweet for tweet in tweets if (float(tweet.created_at.timestamp()) >= ago_31days) & (float(tweet.created_at.timestamp()) <= yd)]
        
        # 一昨日~32日前のツイートを抽出
        dby_32days_tweet = [tweet for tweet in tweets if (float(tweet.created_at.timestamp()) >= ago_32days) & (float(tweet.created_at.timestamp()) <= dby)]

        # 昨日~31日前の内容と日付をlistに格納
        yd_31days_tweet_info = []
        print(len(yd_31days_tweet))
        for tweet in yd_31days_tweet:
            # print(tweet.text)
            # print(tweet.created_at)
            yd_31days_tweet_info.append((tweet.text, tweet.created_at))

        # 一昨日~32日前の内容と日付をlistに格納
        dby_32days_tweet_info = []
        print(len(dby_32days_tweet))
        for tweet in dby_32days_tweet:
            dby_32days_tweet_info.append((tweet.text, tweet.created_at))
        
        return dby_32days_tweet_info, yd_31days_tweet_info

    # exe_per_hour.pyから実行する
    def regularly_get_user_tweets(self, user_id:str, start:float, now_time:float) -> List:

        # start~endの間の「#今日の積み上げ」ツイートを抽出する
        tweets = [tweet for tweet in tweepy.Cursor(TwitterAPI.api.user_timeline, id=user_id).items(limit=500) if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@') & (re.search("#今日の積み上げ", str(tweet.text)) != None) & (float(tweet.created_at.timestamp()) >= float(start)) & (float(tweet.created_at.timestamp()) <= float(now_time))]

        return tweets
    
    def test_get_user_tweets(self, user_id:str, start:float, end:float) -> List:

        # start~endの間の「#今日の積み上げ」ツイートを抽出する
        tweets = [(str(tweet.text), str(tweet.created_at.timestamp())) for tweet in tweepy.Cursor(TwitterAPI.api.user_timeline, id=user_id).items(limit=500) if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@') & (re.search("#今日の積み上げ", str(tweet.text)) != None) & (float(tweet.created_at.timestamp()) >= float(start)) & (float(tweet.created_at.timestamp()) <= float(end))]

        return tweets


    # ツイートを投稿する
    def post_tweet(self, tweet:str) -> None:
        res = TwitterAPI.api.update_status(tweet)
        # print(res)

    
    # DMを送る
    def send_directMessage(self, user_id:str, message:str) -> None:

        # user idからid(整数)を取得する
        recipient_id = TwitterAPI.api.get_user(user_id)

        # DMを送る
        res = TwitterAPI.api.send_direct_message(recipient_id=recipient_id.id_str, text=message)
        # print(res)

    """
        tweet間の期間を計算

        return 
               二つのツイートされた時間の差
    """
    def clu_between_tweets_period(self, created_time1:float, created_time2:float) -> float:
        dif_time = created_time1 - created_time2

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
    
    # id = "HayatoProgram"
    # since = "2021/05/20"
    # until = "2021/06/20"
    # since = datetime(2021,5,20,0,0).strftime("%s")
    # until = datetime(2021,6,20,0,0).strftime("%s")

    # yd = float(until) - 2
    # dby = yd - 86400
    # ago_31days = yd - (86400 * 30)
    # ago_32days = dby - (86400 * 30)
    # print(f'yd:{datetime.fromtimestamp(yd)}')
    # print(f'dby:{datetime.fromtimestamp(dby)}')
    # print(f'ago_31days:{datetime.fromtimestamp(ago_31days)}')
    # print(f'ago_32days:{datetime.fromtimestamp(ago_32days)}')

    # # tweet_info = twitter_api.get_user_tweets(id)
    # dby_32days_tweet_info, yd_31days_tweet_info = twitter_api.get_user_tweets_byTime(id, yd, dby, ago_31days, ago_32days)
    # print(f'dby_32days_tweet_info:{dby_32days_tweet_info}')
    # print(f'yd_31days_tweet_info:{yd_31days_tweet_info}')

    twitter_api.send_directMessage('@kitiyama1152', '月に代わってお仕置きよ ついーとしなさい！')

    