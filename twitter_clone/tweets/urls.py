from django.urls import path
from . import views

urlpatterns = [
    path('tweet_list/', views.tweet_list, name='tweet_list'),
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]

