from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .models import Tweet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Tweet
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'tweets/login.html' 

@login_required
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at') 
    print (tweets)
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})
   
 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'tweets/register.html', {'form': form})
    
    
@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        Tweet.objects.create(user=request.user, content=content)  
        messages.success(request, 'Твит успешно создан!')
        return redirect('tweets/tweet_list.html')  
    












# Create your views here.
