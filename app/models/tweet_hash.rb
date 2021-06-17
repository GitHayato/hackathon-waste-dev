class TweetHash < ApplicationRecord
  belongs_to :user
  validates :tweet_hash, presence: true
  validates :user_id, presence: true
end
