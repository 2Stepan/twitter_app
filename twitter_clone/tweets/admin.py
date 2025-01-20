from django.contrib import admin

from .models import Tweet, Subscription, Like, Comment

# Register your models here.

admin.site.register(Tweet)
admin.site.register(Subscription)
admin.site.register(Like)
admin.site.register(Comment)