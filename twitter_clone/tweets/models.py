from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):  # Модель профиля пользователя, связанная с моделью пользователя
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)  # Поле для биографии пользователя
    # Другие поля профиля

class Follow(models.Model): # Модель для отслеживания подписок пользователей
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')  # Уникальное ограничение для пары "подписчик - подписанный", чтобы предотвратить дублирование

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, default='Untitled')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."


class Like(models.Model):  # Модель для хранения лайков пользователей на твиты
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Пользователь, который поставил лайк
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, default=1)
    
    class Meta:
        unique_together = ('user', 'tweet')  # Ограничение на уникальность (один пользователь может лайкнуть твит только один раз)

    def __str__(self):
        return f"{self.user.username} likes {self.tweet.content}" # Строковое представление объекта лайка

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
           return self.content[:20]  




