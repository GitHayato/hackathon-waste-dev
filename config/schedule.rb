require File.expand_path(File.dirname(__FILE__) + "/environment")

# 実行環境を指定する
set :environment, Rails.env.to_sym
# 実行logの出力先
set :output, "#{Rails.root.to_s}/log/cron.log"

every 15.minutes do
  users = User.all
  users.each do |user|
    hash = user.tweet_hash
    # 引数渡す
    return_value = `python #{Rails.root}/app/controllers/concerns/hackason/exe_per_hour.py
                      -i #{user.nickname} -hv #{hash.tweet_hash} -s #{hash.start_time}
                      -e #{hash.end_time} -c #{hash.count}`
    # 返り値を配列に変換
    return_value = return_value.split(' ')
    # 返り値をもとにTweetHashを更新
    TweetHash.update(tweet_hash: return_value[0], start_time: return_value[1],
                      end_time: return_value[2], count: return_value[3])
  end
end