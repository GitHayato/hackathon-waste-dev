require File.expand_path(File.dirname(__FILE__) + "/environment")
rails_env = ENV['RAILS_ENV'] || :development

# 実行環境を指定する
set :environment, rails_env
# 実行logの出力先
set :output, "#{Rails.root.to_s}/log/cron.log"

every 15.minutes do
  rake 'get_tweets:update_hash_value'
end