class PagesController < ApplicationController
  include TwitterService
  include SessionsHelper
  def index
    if logged_in?
      client = Authorization.init()
      @data = client.search("#今日の積み上げ", result_type: "recent", from: "#{current_user.nickname}").collect do |tweet|
        {
          "image": "#{tweet.user.profile_image_url.to_s.sub('http', 'https')}",
          "name": "#{tweet.user.name}",
          "text": "#{tweet.full_text}",
          "tweet_link": "#{tweet.uri}",
          "create": "#{tweet.created_at.strftime("%H:%M・%Y/%m/%d")}",
          "screen_name": "#{tweet.user.screen_name}"
        }
      end
    end
  end
end
