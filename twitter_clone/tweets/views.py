from django.shortcuts import render, redirect
from django.http import JsonResponse
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
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully!'})
        return JsonResponse({'message': 'Invalid credentials!'}, status=401)
    return render(request, 'tweets/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Проверка на существование пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с такой электронной почтой уже существует.')
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password)
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

def email_confirmation(request):
    email_sent = False
    email = request.GET.get('email')  

    if request.method == 'POST':
        # Логика для повторной отправки письма с подтверждением
        resend_confirmation_email(email)
        email_sent = True
        messages.success(request, 'Письмо с подтверждением было отправлено на вашу электронную почту.')

    return render(request, 'email_confirmation.html', {'email_sent': email_sent, 'email': email})

def resend_confirmation(request):
    # Логика для повторной отправки письма с подтверждением
    email = request.GET.get('email')
    resend_confirmation_email(email)
    messages.success(request, 'Письмо с подтверждением было повторно отправлено на вашу электронную почту.')
    
    return redirect('email_confirmation')  # Перенаправление обратно на страницу подтверждения
def resend_confirmation_email(email):
    # Здесь должна быть ваша логика отправки письма с подтверждением
    pass
# 






# Create your views here.
