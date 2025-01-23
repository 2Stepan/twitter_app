from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    groups = models.ManyToManyField(
       Group,
       related_name='customuser_set',  # Уникальное имя для обратной связи
       blank=True,
       )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True,
   )

class Tweet(models.Model):
    title = models.CharField(max_length=200, default='Untitled')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE, default=1)
    subscribed_to = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.username} -> {self.subscribed_to.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, default=1)

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, default=1)




