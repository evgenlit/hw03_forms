from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from .models import Post, Group, User
from .forms import PostForm


POSTS_COUNT = 10


def index(request):
    title = 'Последние обновления на сайте'
    post_list = Post.objects.select_related('author', 'group')
    paginator = Paginator(post_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'page_obj': posts,
        'title': title
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()
    paginator = Paginator(post_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = User.objects.get(username=username)
    post_list = Post.objects.select_related(
        'author', 'group').filter(
        author__username=username)
    paginator = Paginator(post_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'author': user,
        'page_obj': posts,
        'posts_count': paginator.count
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.select_related(
        'author', 'group').get(pk=post_id)
    author = post.author
    quantity = User.objects.annotate(number_of_entries=Count('posts'))
    context = {
        'post': post,
        'quantity': quantity.get(username=author).number_of_entries
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user)
        context = {
            'form': form,
            'is_edit': False
        }
        return render(request, 'posts/create_post.html', context)
    
    form = PostForm()
    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(instance=post)
    context = {
        'form': form,
        'is_edit': True
    }
    return render(request, 'posts/create_post.html', context)
