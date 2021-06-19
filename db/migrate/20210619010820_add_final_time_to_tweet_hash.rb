class AddFinalTimeToTweetHash < ActiveRecord::Migration[6.0]
  def change
    add_column :tweet_hashes, :final_time, :datetime
  end
end
