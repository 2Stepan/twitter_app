from django.shortcuts import render, redirect
from django.http import JsonResponse,  HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .models import Tweet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.models import User
from django.contrib import messages



@login_required
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')  
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})
 

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('tweet_list.html') 
        else:
            return render(request, 'tweets/login.html', {'error': 'Неверно введенно имя или пароль'})
    return render(request, 'tweets/login.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверка на существование пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('register')

        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
        return redirect('login')  

    return render(request, 'tweets/register.html')




@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        Tweet.objects.create(user=request.user, content=content)  
        messages.success(request, 'Твит успешно создан!')
        return redirect('tweets/tweet_list.html')  






# Create your views here.
