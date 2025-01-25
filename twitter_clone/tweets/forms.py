from django import forms
from .models import CustomUser, Tweet, Comment

class UserSearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100)
    widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Поиск друзей', 'rows': 3}),
        }
    
    

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password'] 
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Имя пользователя', 
            'email': 'Электронная почта',
            'password': 'Пароль', # Убираем метку для текстового поля
        }
        
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Что нового?)', 'rows': 3}),
        }
        labels = {
            'content': '', 
        }
        
class CommentForm(forms.ModelForm):  # Указываем модель, к которой относится форма 
    class Meta:
        model = Comment
        fields = ['content']  # Поля формы
        
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '', 'rows': 3}),  # Настраиваем виджет для текстового поля
        }
        labels = {
            'content': '',   # Убираем метку для текстового поля
        }
