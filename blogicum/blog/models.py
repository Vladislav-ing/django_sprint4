from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import TotalPublishCreate
from core.utils import PostsQuerySet

from . import constants

UserModel = get_user_model()


class Location(TotalPublishCreate):
    """Модель для локационных меток."""

    name = models.CharField(
        max_length=constants.TITLE_FIELD_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        default_related_name = 'locations_posts'
        ordering = ('name', )

    def __str__(self):
        return self.name[:constants.DISPLAY_LENGTH]


class Category(TotalPublishCreate):
    """Модель для определения категории поста."""

    title = models.CharField(
        max_length=constants.TITLE_FIELD_LENGTH, blank=True,
        verbose_name='Заголовок'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(
        unique=True, verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'
        ordering = ('slug', )

    def __str__(self):
        return self.title[:constants.DISPLAY_LENGTH]


class Post(TotalPublishCreate):
    """
    Основная модель, содержащая подробную информацию о посте.
    Также, в данной модели выстраено
    отношение N:1 к модели категории, локации.
    """

    title = models.CharField(
        max_length=constants.TITLE_FIELD_LENGTH, verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE,
        verbose_name='Автор публикации', related_name='author_posts'
    )
    location = models.ForeignKey(
        Location, blank=True, on_delete=models.SET_NULL,
        null=True, verbose_name='Местоположение',
        related_name='loc_posts'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField(
        'Изображение', blank='True',
        upload_to='post_imagine')

    objects = models.Manager()

    custom_manager = PostsQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.title[:constants.DISPLAY_LENGTH]

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.pk})


class Comment(TotalPublishCreate):
    """Модель комментария. Создание, редактирование, удаление."""

    author = models.ForeignKey(
        UserModel, verbose_name='Автор комментария',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post, verbose_name='Комментируемый пост',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at', )
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:constants.DISPLAY_LENGTH]
