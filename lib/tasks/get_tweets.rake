namespace :get_tweets do
  desc 'pythonを実行し、その返り値をもとにTweetHashを更新する'
  task update_hash_value: :environment do
    users = User.all
    users.each do |user|
      hash = user.tweet_hash
      before_update = []
      # 配列に更新前の値を保存
      before_update.append(hash.tweet_hash, hash.start_time, hash.end_time, hash.count)
      # 引数渡す
      return_value = `python #{Rails.root}/app/controllers/concerns/hackason/exe_per_hour.py -i #{user.nickname} -hv #{hash.tweet_hash} -s #{hash.start_time} -e #{hash.end_time} -c #{hash.count}`
      # 返り値を配列に変換
      return_value = return_value.split(' ')
      # 更新処理
      hash.update(tweet_hash: return_value[0], start_time: return_value[1],
                    end_time: return_value[2], count: return_value[3])
      Rails.application.config.another_logger.info("
        ======
        #{user.nickname}
        実行前 hash_value: #{before_update[0]} start_time: #{before_update[1]} end_time: #{before_update[2]} count: #{before_update[3]}
        実行後 hash_value: #{return_value[0]} start_time: #{return_value[1]} end_time: #{return_value[2]} count: #{return_value[3]}
        ======
      ")
    end
  end
end
