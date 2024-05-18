from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, ListView,
                                  UpdateView)

from .constants import AMOUNT_POSTS
from .forms import CommentForm, PostForm, UserEditForm
from .mixins import AuthorMixin, CommentMixin, PostMixin
from .models import Category, Comment, Post

User = get_user_model()


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = AMOUNT_POSTS
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        self.profile = get_object_or_404(
            User, username=self.kwargs['username'])

        if self.request.user == self.profile:
            return (Post.objects.posts_annotate()
                    .filter(author=self.profile))

        return (Post.objects
                .posts_published()
                .posts_annotate()
                .filter(author=self.profile))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={
                'username': self.get_object().username})


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={
                'username': self.request.user.username})


class PostUpdateView(AuthorMixin, PostMixin, UpdateView):
    form_class = PostForm


class IndexPostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = AMOUNT_POSTS

    def get_queryset(self):
        return (Post.objects
                .posts_published()
                .posts_annotate())


class PostDeleteView(AuthorMixin, PostMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = PostForm(instance=post)
        context['post'] = post
        return context


def post_detail(request, post_id):
    template_path = 'blog/detail.html'
    post = get_object_or_404(Post, pk=post_id)
    category = get_object_or_404(Category, pk=post.category_id)
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.all()
    }

    if (request.user == post.author
        or (post.is_published and category.is_published
            and post.pub_date <= timezone.now())):
        return render(request, template_path, context)

    raise Http404


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = (get_object_or_404(
            Post, pk=self.kwargs['post_id']).id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.kwargs['post_id']})


class CommentUpdateView(AuthorMixin, CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDelete(AuthorMixin, CommentMixin, DeleteView):
    pass


def category_posts(request, category_slug):
    template_path = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug,
        is_published=True
    )
    posts_list = (
        Post.objects
        .posts_published()
        .posts_annotate()
        .filter(category=category)
    )
    paginator = Paginator(posts_list, AMOUNT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, template_path, context)
