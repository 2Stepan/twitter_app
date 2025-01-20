from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    title = models.CharField(max_length=200, default='Untitled')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}..."

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




