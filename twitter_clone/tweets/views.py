from django.shortcuts import render, redirect
from .models import Tweet
from django.contrib.auth.decorators import login_required
from .models import Tweet, Follow, CustomUser, Comment, Like
from .forms import CustomUserCreationForm, TweetForm, CommentForm, UserSearchForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,  HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage 
from django.shortcuts import redirect, get_object_or_404
import json
from django.contrib.auth import authenticate, login



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

@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(CustomUser, id=user_id)
    Follow.objects.get_or_create(follower=request.user, followed=followed_user)
    return redirect('user_search')  # Или на страницу профиля

def user_search(request):
    form = UserSearchForm()
    results = []
    
    if request.method == 'GET' and 'query' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = CustomUser.objects.filter(username__icontains=query) | CustomUser.objects.filter(first_name__icontains=query) | CustomUser.objects.filter(last_name__icontains=query)

    return render(request, 'tweets/user_search.html', {'form': form, 'results': results})


@login_required
def user_profile(request, user_id):
    user = request.user  # Получаем текущего пользователя
    user = get_object_or_404(CustomUser, id=user_id)
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # Устанавливаем текущего пользователя как автора твита
            tweet.save()
            return redirect('user_profile')  # Перенаправляем на ту же страницу после публикации
    else:
        form = TweetForm()
        
    return render(request, 'tweets/user_profile.html', {'user': user, 'tweets': tweets, 'form': form})


@login_required
def tweet_list(request):
    template_name = 'tweet_list.html'  # Укажите ваш шаблон 
    tweets = Tweet.objects.all().order_by('-created_at').prefetch_related('like_set')   # Получаем все твиты, сортируем по дате создания (от новых к старым) и подгружаем связанные лайки
    paginator = Paginator(tweets, 5)  # Создаем пагинатор, чтобы отображать 5 твитов на странице

    page_number = request.GET.get('page')   # Получаем номер страницы из GET-запроса

    try: 
        page_obj = paginator.page(page_number)   # Пытаемся получить объекты для указанной страницы
    except PageNotAnInteger: 
        page_obj = paginator.page(1)  # Если номер страницы не является целым числом, показываем первую страницу
    except EmptyPage: 
        page_obj = paginator.page(paginator.num_pages)   # Если страница пустая, показываем последнюю страницу

    if request.method == 'POST': 
        form = CommentForm(request.POST)  # Если запрос POST, создаем форму для комментария с данными из запроса
        if form.is_valid():   # Если форма валидна, сохраняем комментарий без немедленного сохранения в БД
            comment = form.save(commit=False) 
            comment.user = request.user    # Устанавливаем текущего пользователя как автора комментария
            tweet_id = request.POST.get('tweet_id') # Получаем ID твита из POST-запроса 
            comment.tweet = Tweet.objects.get(id=tweet_id) # Привязываем комментарий к соответствующему твиту
            comment.save() # Сохраняем комментарий в БД
            return redirect('tweet_list')  # Перенаправляем на страницу со списком твитов
    else: 
        form = CommentForm()   # Если запрос не POST, создаем пустую форму для комментария

    return render(request, 'tweets/tweet_list.html', { 
        'tweets': page_obj.object_list,  
        'form': form, 
        'page_obj': page_obj  
    })
    
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id) # Получаем комментарий по его ID или возвращаем 404, если он не найден
    
    if request.method == 'POST': 
        form = CommentForm(request.POST, instance=comment)  # Если запрос POST, создаем форму с данными комментария
        if form.is_valid():
            form.save() # Сохраняем изменения в комментарии
            return redirect('tweet_list')
    else:    # Если запрос не POST, создаем форму с текущими данными комментария
        form = CommentForm(instance=comment)

    return render(request, 'tweets/edit_comment.html', {'form': form})  # Отображаем шаблон для редактирования комментария

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment.delete()  # Удаляем комментарий из БД
        return redirect('tweet_list')  # Перенаправляем на страницу со списком твитов

    return render(request, 'tweets/delete_comment.html', {'comment': comment})

  
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)   # Если запрос POST, создаем форму для нового твита с данными из запроса
        if form.is_valid():
            form.save() # Сохраняем новый твит в БД
            return redirect('tweet_list')    # Перенаправляем на страницу со списком твитов
    else: # Если запрос не POST, создаем пустую форму для нового твита
        form = TweetForm()
    
    return render(request, 'tweets/create_tweet.html', {'form': form})
   
 

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
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id) # Получаем твит по его ID или возвращаем 404, если он не найден
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet) # Пытаемся получить лайк пользователя на этот твит; если не существует, создаем новый
    if not created:
        # Если лайк уже существует, удаляем его
        like.delete()  
    return redirect('tweet_list') # Перенаправляем пользователя на страницу со списком твитов

@login_required
def unlike_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)  # Получаем твит по его ID или возвращаем 404, если он не найден
    try:
        like = Like.objects.get(user=request.user, tweet=tweet)  # Пытаемся получить лайк пользователя на этот твит
        like.delete() # Удаляем найденный лайк
    except Like.DoesNotExist:  # Если лайка не существует, ничего не делаем (просто продолжаем)
        pass
    return redirect('tweet_list')   # Перенаправляем пользователя на страницу со списком твитов
    

    












# Create your views here.
