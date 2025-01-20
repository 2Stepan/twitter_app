from django.urls import path
from . import views





urlpatterns = [
    path('tweet_list.html', views.tweet_list, name='tweet_list'),
    path('', views.login_view, name='login'),
    path('register.html', views.register, name='register'),
     path('email-confirmation/', views.email_confirmation, name='email_confirmation'),
    path('resend-confirmation/', views.resend_confirmation, name='resend_confirmation'),
]

