from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import Category, Location, Post

admin.site.unregister(User)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    empty_value_display = 'Значение не выбрано.'
    list_display = (
        'is_published', 'pub_date', 'title',
        'text', 'author', 'category', 'location'
    )
    list_editable = (
        'is_published', 'pub_date',
        'text', 'category', 'location'
    )
    search_fields = ('title', )
    list_filter = (
        'is_published', 'category',
        'pub_date', 'author'
    )
    list_display_links = ('title', )


class LocationInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('title', 'is_published', 'category', 'pub_date', 'location')
    readonly_fields = ('title', 'category')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        LocationInline,
    )
    list_display = (
        'name', 'is_published', 'created_at'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'num_posts')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def num_posts(self, obj):
        return obj.author_posts.count()


admin.site.unregister(Group)
