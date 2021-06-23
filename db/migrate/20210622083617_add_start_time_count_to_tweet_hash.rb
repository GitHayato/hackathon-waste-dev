class AddStartTimeCountToTweetHash < ActiveRecord::Migration[6.0]
  def change
    add_column :tweet_hashes, :start_time, :datetime
    add_column :tweet_hashes, :count, :integer

  end
end
