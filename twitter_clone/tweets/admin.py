from django.contrib import admin
from .models import Tweet, Like, Comment, CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tweet)
admin.site.register(Like)
admin.site.register(Comment)