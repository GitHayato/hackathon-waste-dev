import hashlib


# ツイート、タイムスタンプ、前のブロックのhash値を全て結合する。
def combineIntoOne(tweet:str, timestamp:str, prehash_Value:str) -> str:
    try:
        block = tweet + timestamp + prehash_Value
    except Exception as e:
        print(f'error:{e}')

    return  block


# sha256に変換する
def implement_hashing(tweet:str, timestamp:str, prehash_Value:str) -> str:
    block = combineIntoOne(tweet, timestamp, prehash_Value)
    try:
        s256 = hashlib.sha256(block.encode()).hexdigest()
    except Exception as e:
        print(f'error:{e}')
    
    return s256


if __name__ == "__main__":
    text = "test"
    text_1 = "a"
    text_2 = "b"
    hash_valuse = implement_hashing(text, text_1, text_2)
    print(hash_valuse)
    print(len(hash_valuse))