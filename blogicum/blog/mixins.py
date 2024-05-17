from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comment, Post


# Authorization
class AuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        object = self.get_object()
        return redirect(
            reverse(
                'blog:post_detail',
                kwargs={
                    'post_id': object.id}))


# Excluse IndexList
class PostMixin:
    model = Post
    template_name = 'blog/create.html'


# Exclude Create
class CommentMixin:
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.get_object().post_id})
