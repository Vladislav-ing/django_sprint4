from django.core.paginator import Paginator

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView)

from django.shortcuts import get_object_or_404, render

from django.http import Http404

from django.utils import timezone

from django.urls import reverse, reverse_lazy

from .constants import AMOUNT_POSTS
from .forms import PostForm, UserEditForm, CommentForm
from .models import Category, Post, Comment
from .mixins import AuthorMixin, PostMixin, CommentMixin

User = get_user_model()


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username'])

        if (self.request.user.username 
            == self.kwargs['username']):
            posts = Post.with_comment_count_author().filter(author=self.request.user)
        else:
            posts = Post.with_comment_count_all().filter(
                author=context['profile'])

        paginator = Paginator(posts, AMOUNT_POSTS)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
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
        form.instance.is_published = True
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
        return Post.with_comment_count_all()


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

    if request.user.username == post.author.username:
        return render(request, template_path, context)

    if not (post.is_published
            and category.is_published
            and post.pub_date <= timezone.now()):
        raise Http404

    return render(request, template_path, context)


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.post_obj.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.post_obj.id})


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
        Post.with_comment_count_all().filter(category=category)
    )
    paginator = Paginator(posts_list, AMOUNT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, template_path, context)
