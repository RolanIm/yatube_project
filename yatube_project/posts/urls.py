from . import views
from django.urls import path

app_name = 'posts'
urlpatterns = [
    path(
        '',
        views.PostListView.as_view(),
        name='post_list'
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'create/',
        views.PostCreateView.as_view(),
        name='post_create'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'posts/<int:pk>/edit',
        views.PostUpdateView.as_view(),
        name='post_edit'
    ),
    path(
        'group/<slug>/',
        views.GroupListView.as_view(),
        name='group_posts'
    ),
    path(
        'posts/<int:pk>/comment',
        views.CommentCreateView.as_view(),
        name='add_comment'

    ),
    path(
        'posts/<int:pk>/comment/delete',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        'follow/',
        views.FollowListView.as_view(),
        name='follow_list'
    ),
    path(
        'profile/<str:username>/follow/',
        views.ProfileFollowView.as_view(),
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.ProfileUnfollowView.as_view(),
        name="profile_unfollow"
    ),
]
