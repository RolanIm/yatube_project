from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from .models import Post, Group, User
from .forms import CommentForm
from django.views.generic import (CreateView, UpdateView,
                                  ListView, DetailView)


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'posts/post_list.html'


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
