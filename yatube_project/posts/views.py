from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.urls import reverse_lazy


def index(request):
    all_posts = Post.objects.all().order_by('-pub_date')
    page_obj, paginator = get_page_objects(request, posts=all_posts, catch_len=300, max_len=310)

    context = {
        'page_obj': page_obj,
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    all_posts = Post.objects.filter(group=group).order_by('-pub_date')
    page_obj, paginator = get_page_objects(request, posts=all_posts, catch_len=300, max_len=310)
    group = get_object_or_404(Group, slug=slug)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


@login_required
def profile(request, username):
    all_posts_user = Post.objects.filter(author__username=username).order_by('-pub_date')
    page_obj, paginator = get_page_objects(request, posts=all_posts_user, catch_len=300, max_len=310)
    author_obj = User.objects.filter(username=username)[0]
    count_posts = paginator.count

    context = {
        'page_obj': page_obj,
        'author_obj': author_obj,
        'count_posts': count_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    count_posts = Post.objects.filter(author=post.author).count()
    title_text = post.text[:30]

    context = {
        'post': post,
        'count_posts': count_posts,
        'title_text': title_text,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


def post_edit():
    pass


def get_page_objects(request, posts, catch_len=-1, max_len=-1):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for page in page_obj:
        if len(page.text) > max_len:
            page.text = page.text[:catch_len] + '...'
    return page_obj, paginator
