from . import views
from django.urls import path

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug>/', views.group_posts, name='group_posts'),
]
