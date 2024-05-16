from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.IndexPostListView.as_view(),
        name='index'),
    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post_detail'),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'),
    path(
        'posts/<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.CommentDelete.as_view(),
        name='delete_comment'),
    path(
        'profile/edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'),
    path(
        'profile/<slug:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'),
]
