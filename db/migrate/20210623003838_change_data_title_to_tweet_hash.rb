class ChangeDataTitleToTweetHash < ActiveRecord::Migration[6.0]
  def change
    add_column :tweet_hashes, :end_time, :float
    change_column :tweet_hashes, :start_time, :float
  end

end
