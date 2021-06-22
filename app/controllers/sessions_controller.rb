class SessionsController < ApplicationController
  include SessionsHelper
  def create
    unless request.env['omniauth.auth'][:uid]
      flash[:danger] = '連携に失敗しました'
      redirect_to root_url
    end
    user_data = request.env['omniauth.auth']
    user = User.find_by(uid: user_data[:uid])
    file = File.dirname(__FILE__)
    if user
      log_in user
      hash = TweetHash.find_by(user_id: user.id)
      tweet_hash = `python #{file}/concerns/hackason/second_main.py -i #{user.nickname} -phv #{hash}`
      TweetHash.update(tweet_hash: tweet_hash)
      flash[:success] = 'ログインしました'
      redirect_to root_url
    else
      new_user = User.new(
        uid: user_data[:uid],
        nickname: user_data[:info][:nickname],
        name: user_data[:info][:name],
        image: user_data[:info][:image],
      )
      if new_user.save
        log_in new_user
        tweet_hash = `python #{file}/concerns/hackason/first_main.py -i #{new_user.nickname}`
        TweetHash.create(tweet_hash: tweet_hash, user_id: new_user.id)
        flash[:success] = 'ユーザー登録成功'
      else
        flash[:danger] = '予期せぬエラーが発生しました'
      end
      redirect_to root_url
    end
  end


  def destroy
    log_out if logged_in?
    flash[:success] = 'ログアウトしました'
    redirect_to root_url
  end
end