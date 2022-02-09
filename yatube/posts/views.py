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
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    template = 'posts/profile.html'
    paginator = Paginator(post_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'author': user,
        'page_obj': posts,
        'posts_count': paginator.count
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    quantity = User.objects.annotate(number_of_entries=Count('posts'))
    context = {
        'post': post,
        'quantity': quantity.get(username=author).number_of_entries
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', username=request.user)
    form = PostForm()
    context = {
        'form': form,
        'id_edit': False,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    template = 'posts/create_post.html'
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': True,
        'post': post
    }
    return render(request, template, context)
