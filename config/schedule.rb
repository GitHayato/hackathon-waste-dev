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
    return_value = command "python #{Rails.root}/app/controllers/concerns/hackason/exe_per_hour.py -i #{user.nickname} -hv #{hash.tweet_hash} -s #{hash.start_time} -e #{hash.end_time} -c #{hash.count}"
    TweetHash.update(tweet_hash: hash.tweet_hash, start_time: hash.start_time, end_time: hash.end_time, count: hash.count)
  end
end