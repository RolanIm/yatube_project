from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    all_posts = Post.objects.all().order_by('-pub_date')  # all posts order by publication date DESC
    paginator = Paginator(all_posts, 10)  # show 10 posts on each page
    page_number = request.GET.get('page')  # get page number
    page_obj = paginator.get_page(page_number)  # get posts by page number
    context = {
        'page_obj': page_obj,
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    all_posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(all_posts, 10)  # show 10 posts on page
    page_number = request.GET.get('page')  # get page number
    page_obj = paginator.get_page(page_number)  # get posts by page number
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)
