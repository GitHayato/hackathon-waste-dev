class CreateTweetHashes < ActiveRecord::Migration[6.0]
  def change
    create_table :tweet_hashes do |t|
      t.string      :tweet_hash, null: false
      t.references  :user, foreign_key: true
      t.timestamps
    end
  end
end
