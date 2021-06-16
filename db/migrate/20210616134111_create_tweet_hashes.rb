class CreateTweetHashes < ActiveRecord::Migration[6.0]
  def change
    create_table :tweet_hashes do |t|

      t.timestamps
    end
  end
end
