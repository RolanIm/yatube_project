from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from .models import Post, Group, User
from .forms import CommentForm
from django.views.generic import (CreateView, UpdateView, DeleteView,
                                  ListView, DetailView)


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/post_list.html'

# def index(request):
#     all_posts = Post.objects.all().order_by('-pub_date')
#     page_obj, paginator = get_page_objects(request, posts=all_posts)
#
#     context = {
#         'page_obj': page_obj,
#     }
#     template = 'posts/index.html'
#     return render(request, template, context)


class GroupListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/group_list.html'

    def get_queryset(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return Post.objects.filter(group=self.group).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.group
        return context

# def group_posts(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     all_posts = Post.objects.filter(group=group).order_by('-pub_date')
#     page_obj, paginator = get_page_objects(request, posts=all_posts)
#
#     context = {
#         'group': group,
#         'page_obj': page_obj,
#     }
#     template = 'posts/group_list.html'
#     return render(request, template, context)


class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/profile.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        user_posts = Post.objects.filter(author__username=self.user.username)
        return user_posts.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_obj'] = self.user
        return context

# @login_required
# def profile(request, username):
#     user_posts = Post.objects.filter(author__username=username)
#     all_posts_user = user_posts.order_by('-pub_date')
#     page_obj, paginator = get_page_objects(request, posts=all_posts_user)
#     author_obj = User.objects.filter(username=username)[0]
#     count_posts = paginator.count
#
#     context = {
#         'page_obj': page_obj,
#         'author_obj': author_obj,
#         'count_posts': count_posts,
#     }
#     return render(request, 'posts/profile.html', context)


class PostDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        if args:
            pk = args[0]
        else:
            pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        count_posts = Post.objects.filter(author=post.author).count()
        title_text = post.text[:30]
        form = CommentForm()

        context = {
            'form': form,
            'post': post,
            'comments': comments,
            'count_posts': count_posts,
            'title_text': title_text,
        }
        return render(request, 'posts/post_detail.html', context)


# def post_detail(request, post_id):
#     post = Post.objects.get(pk=post_id)
#     comments = post.comments.all()
#     if request.user.is_authenticated:
#         form = CommentForm()
#     else:
#         form = None
#     count_posts = Post.objects.filter(author=post.author).count()
#     title_text = post.text[:30]
#
#     context = {
#         'form': form,
#         'post': post,
#         'comments': comments,
#         'count_posts': count_posts,
#         'title_text': title_text,
#     }
#     return render(request, 'posts/post_detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['text', 'group', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

    def get_success_url(self):
        success_url = reverse(
            'posts:profile',
            args=[self.request.user.username]
        )
        return success_url


# @login_required
# def post_create(request):
#     form = PostForm(
#         request.POST or None,
#         files=request.FILES or None
#     )
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.author = request.user
#         post.save()
#         return redirect(reverse('posts:profile', args=[post.author.username]))
#     context = {
#         'form': form,
#     }
#     return render(request, 'posts/create_post.html', context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['text', 'group', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        post = super().get_object()
        if self.request.user != post.author:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_success_url(self):
        success_url = reverse(
            'posts:profile',
            args=[self.request.user.username]
        )
        return success_url


# @login_required
# def post_edit(request, post_id):
#     post = get_object_or_404(Post, pk=post_id, author=request.user)
#     form = PostForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=post
#     )
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.author = request.user
#         post.save()
#         return redirect(reverse('posts:profile', args=[post.author.username]))
#
#     form = PostForm(instance=post)
#     context = {
#         'form': form,
#         'post': post,
#         'is_edit': True
#     }
#     return render(request, 'posts/create_post.html', context)


# def get_page_objects(request, posts):
#     paginator = Paginator(posts, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return page_obj, paginator


class CommentCreateView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        if args:
            pk = args[0]
        else:
            pk = kwargs.get('pk')
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(pk=pk)
            comment.save()
            return redirect(reverse('posts:post_detail', args=[pk]))
        return render(
            request,
            reverse('posts:post_detail', args=[pk]),
            context={'form': form}
        )

# @login_required
# def add_comment(request, post_id):
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.author = request.user
#         comment.post = Post.objects.get(pk=post_id)
#         comment.save()
#     return redirect(reverse('posts:post_id', args=[post_id]))
