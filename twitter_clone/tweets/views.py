from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .models import Tweet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, TweetForm
from django.core.paginator import Paginator

@login_required
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    paginator = Paginator(tweets, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')  # Перенаправление на ту же страницу после добавления твита
    else:
        form = TweetForm()

    return render(request, 'tweets/tweet_list.html', {
        'tweets': tweets,
        'form': form,
        'page_obj': page_obj
    })

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
            return HttpResponseRedirect(redirect('tweet_list').url)  # Перенаправление на маршрут
        else:
            return render(request, 'tweets/login.html', {'error': 'Неверно введенно имя или пароль'})
    return render(request, 'tweets/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
            return redirect('login')  # Перенаправление на маршрут
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, проверьте введенные данные.')
            print(form.errors)  # Вывод ошибок валидации в терминал
    else:
        form = CustomUserCreationForm()
    return render(request, 'tweets/register.html', {'form': form})