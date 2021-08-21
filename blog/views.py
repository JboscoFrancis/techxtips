from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group, auth
from django.db import IntegrityError
import json
from .forms import PostForm, CommentForm, UserRegistrationForm
from .models import Post, Comment, News, Subscriber, Reply, Tips

# Create your views here.
def index(request):
    post = Post.objects.all().order_by('date_created')[:4]
    tips = Tips.objects.all().order_by('-date_created')
    context = {'post':post, 'tips':tips}
    return render(request, 'blog/index.html', context)
    
def service(request):
    return render(request, 'blog/service.html')

def contact(request):
    return render(request, 'blog/contact.html')

def account(request):
    return render(request, 'blog/account.html')

def userlogin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'thank you for signing in TechxTips')
            return redirect('index')
        else:
            messages.warning(request, f'Sorry username or password is incorrect')
            return redirect('userlogin')
    return render(request, 'blog/login.html')

def userlogout(request):
    logout(request)
    return redirect('index')

def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = first_name.lower()

            fullname = first_name + ' ' + last_name
            try:
                user = User.objects.create_user(
                    username = email, first_name= first_name, last_name=last_name, email = email, password=password
                )
                user.save()
                try:
                    subscriber = Subscriber.objects.create(
                        name = fullname, email=email
                    )
                    subscriber.save()
                except IntegrityError:
                    pass

                return redirect('userlogin')
            except IntegrityError:
                messages.info(request, f'Sorry the email already used by someone')
    context = {'form': form}
    return render(request, 'blog/register.html', context)

def blog(request):
    post = Post.objects.all().order_by('-date_created')
    news = News.objects.all().order_by('-date_created')[:4]
    if request.method == 'POST':
        q = request.POST['search']
        # post = Post.objects.filter(title__search = q)
        post = Post.objects.filter(title__icontains = q)
        if post:
            pass
        else:
            messages.info(request, f'Oop!! no result found')
    
    paginator = Paginator(post, 5)     #post pagination
    page_num = request.GET.get('page')
    post = paginator.get_page(page_num)
    context = {'post': post, 'news': news}
    return render(request, 'blog/blog.html', context)

def post(request, slug):
    form = CommentForm()
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post)
    totalcomment = Comment.objects.filter(post=post).count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                return JsonResponse({'name':new_comment.user.username, 'comment_msg':new_comment.text})
            else:
                messages.warning(request, f'Oops! plz login')
    context = {'post': post, 'form': form, 'comments':comments, 'totalcomment':totalcomment}
    return render(request, 'blog/post.html', context)

def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('blog')
    context = {'form': form}
    return render(request, 'blog/create_post.html', context)

def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('blog')
    context = {'form': form}
    return render(request, 'blog/update_post.html', context)

@csrf_exempt
def reply(request):
    if request.method == 'POST':
        replycommentId = request.POST['commentId']
        replytext = request.POST['replytext']
        comment = Comment.objects.get(id=replycommentId)
        user = request.user
        reply = Reply.objects.create(
            user=user, comment=comment, text = replytext
        )
        reply.save()
        print('-----------------')
        return JsonResponse('data-sent', safe=False)

@csrf_exempt
def likepost(request):
    if request.method == 'POST':
        postId = request.POST['postId']
        post = Post.objects.get(id=postId)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.save()
            count = post.likes_count
            print(count)
            result = count
        else:
            post.likes.add(request.user)
            post.save()
            count = post.likes_count
            print(count)
            result = count
    return JsonResponse({'result': result, })

@csrf_exempt
def subscribe(request):
    message1 = ''
    message2 = ''
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        try:
            subscriber = Subscriber.objects.create(
                name = name, email=email
            )
            subscriber.save()
            message1 = 'You have subscribed successfull'
        except IntegrityError:
            message2 = 'Opp!! This email already exist'
    return JsonResponse({'message1': message1, 'message2': message2,})

def tips(request):
    return render(request, 'blog/tips.html')


def tips_detail(request, title, pk):
    tip = Tips.objects.get(id=pk)
    context = {'tip':tip}
    return render(request, 'blog/tips_detail.html',context)
