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

from hashing.hashingBysha256 import implement_hashing
from twitter_api.get_tweet import TwitterAPI


def main(user_id:str):
    # 今までの「積み上げ」ツイート(内容、日付)を取得
    twitter_api = TwitterAPI()


    # Hayato君のアカウント試しに使わせて貰ってます笑
    # id = "HayatoProgram"
    tweet_info = twitter_api.get_user_tweets(user_id)
    
    # それらをhash化する
    pre_block = "test"
    for i,info in enumerate(tweet_info):
        hash_valuse = implement_hashing(info[0], str(info[1]), pre_block)

        # 最後の要素の時実行
        if i == len(tweet_info) - 1:
            return hash_valuse

        # 前のブロック値を更新
        pre_block = hash_valuse
        


if __name__ == "__main__":
    # ユーザーのIDを受け取る
    user_id = str(input())

    # mainを実行
    hash_block = main(user_id)
    
    # Rubyにhash値を返す
    print(hash_block)
