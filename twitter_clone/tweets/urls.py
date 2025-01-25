from django.urls import path
from . import views
from .views import  login_view, create_tweet, user_search, follow_user, delete_comment, edit_comment, like_tweet, unlike_tweet, edit_tweet,delete_tweet





urlpatterns = [
    path('', login_view, name='login'),
    path('register/', views.register, name='register'),
    path('tweet_list.html', views.tweet_list, name='tweet_list'),
    path('create/', create_tweet, name='create_tweet'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('search/', user_search, name='user_search'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('tweet/<int:tweet_id>/like/', like_tweet, name='like_tweet'),
    path('tweet/<int:tweet_id>/unlike/', unlike_tweet, name='unlike_tweet'),
    path('edit_tweet/<int:tweet_id>/', edit_tweet, name='edit_tweet'),
    path('delete_tweet/<int:tweet_id>/',delete_tweet,name='delete_tweet'),
]

