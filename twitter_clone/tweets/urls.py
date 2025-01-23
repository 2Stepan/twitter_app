from django.urls import path
from . import views
from .views import  CustomLoginView





urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]

