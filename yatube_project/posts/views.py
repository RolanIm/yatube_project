from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    template = 'posts/index.html'
    title = '<h4>Это главная страница проекта Yatube</h4>'
    context = {'title': title}
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    title = '<h4>Здесь будет информация о группах проекта Yatube</h4>'
    context = {'title': title}
    return render(request, template, context)
