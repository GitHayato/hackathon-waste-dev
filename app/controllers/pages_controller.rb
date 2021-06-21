class PagesController < ApplicationController
  include TwitterService
  include SessionsHelper
  def index
    if logged_in?
      @data = data(current_user.nickname, "#今日の積み上げ")
    end
    @punishments = data("tukikawaoshioki", "#お仕置き執行")
    @rewards = data("taiyogohoubi", "")
  end

  private

  def data(user, tag)
    client = Authorization.init()
    data = client.search(tag, result_type: "recent", from: user).collect do |tweet|
      {
        "image": "#{tweet.user.profile_image_url.to_s.sub('http', 'https')}",
        "name": "#{tweet.user.name}",
        "text": "#{tweet.full_text}",
        "tweet_link": "#{tweet.uri}",
        "create": "#{tweet.created_at.in_time_zone('Tokyo').strftime("%H:%M・%Y/%m/%d")}",
        "screen_name": "#{tweet.user.screen_name}"
      }
    end
    return data
  end
end
