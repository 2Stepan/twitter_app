from django import forms
from .models import CustomUser, Tweet

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password'] 
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Что у вас на уме?', 'rows': 3}),
        }