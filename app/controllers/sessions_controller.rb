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
        value = `python #{file}/concerns/hackason/first_main.py -i #{new_user.nickname}`
        value = value.split(' ')
        tweet_hash = TweetHash.new(tweet_hash: value[0], user_id: new_user.id, start_time: value[1], end_time: value[2], count: value[3])
        if tweet_hash.save
          # 変数tweet_hashが正しく保存されるとき、ログインする
          log_in new_user
          flash[:success] = 'ユーザー登録成功'
        else
          # 変数tweet_hashが正しく保存されないとき、ユーザーの情報を削除する
          new_user.destroy
          flash[:danger] = "予期せぬエラーが発生しました"
        end
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