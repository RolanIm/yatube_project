from . import views
from django.urls import path

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug>/', views.group_posts, name='group_posts'),
    path('create/', views.post_create, name='post_create'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_id'),
    path('posts/<int:post_id>/edit', views.post_edit, name='post_edit'),
]
