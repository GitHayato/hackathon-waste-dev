class UsersController < ApplicationController
  include SessionsHelper
  def destroy
    current_user.destroy
    redirect_to root_path
    flash[:success] = '正常に退会されました、ありがとうございました!'
  end
end
