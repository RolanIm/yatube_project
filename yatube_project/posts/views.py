from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('The main page of the Yatube project.')


def group_posts(request, slug):
    return HttpResponse(f'Posts group by {slug}.')
