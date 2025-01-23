from django.urls import path
from . import views





urlpatterns = [
    path('tweet_list.html', views.tweet_list, name='tweet_list'),
    path('', views.login_view, name='login'),
    path('register.html', views.register, name='register'),
]

