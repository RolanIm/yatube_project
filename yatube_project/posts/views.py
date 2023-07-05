from django.shortcuts import render, get_object_or_404
from .models import Post, Group, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    all_posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for page in page_obj:
        if len(page.text) > 310:
            page.text = page.text[:300] + '...'

    context = {
        'page_obj': page_obj,
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    all_posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for page in page_obj:
        if len(page.text) > 310:
            page.text = page.text[:300] + '...'

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


def profile(request, username):
    all_posts_user = Post.objects.filter(author__username=username).order_by('-pub_date')
    paginator = Paginator(all_posts_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    author_obj = User.objects.filter(username=username)[0]
    count_posts = paginator.count

    for page in page_obj:
        if len(page.text) > 310:
            page.text = page.text[:300] + '...'

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


def post_create(request):
    pass
