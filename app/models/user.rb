class User < ApplicationRecord
  has_one :tweet_hashes
end
