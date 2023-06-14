from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('<h1>The main page of the Yatube project.<h1>'
                        '<p>About</p>'
                        '<h2>There will be posts about'
                            '<ul>'
                                '<li><a href="https://i.pinimg.com/originals/aa/d2/99/aad2991ed6b54233f382d5a12a01d61d.jpg" target="_blank">dogs</a></li>'
                                '<li><a href="https://ferret-pet.ru/wp-content/uploads/4/1/c/41c114082ccae8adaee31f4f6e797d2b.jpeg" target="_blank">cats</a></li>'
                                '<li><i>people</i></li>'
                            '</ul>'
                        '</h2>')


def group_posts(request, slug):
    return HttpResponse(f'Posts group by {slug}.')
