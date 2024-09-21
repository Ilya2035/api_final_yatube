"""Модуль для регистрации моделей в админ-панели Django."""

from django.contrib import admin
from .models import Group, Follow, Post, Comment


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Администрирование модели Group."""

    list_display = ('title', 'slug',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Администрирование модели Follow."""

    list_display = ('user', 'following')
    search_fields = ('user__username', 'following__username')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Администрирование модели Post."""

    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Администрирование модели Comment."""

    list_display = ('pk', 'text', 'created', 'author', 'post')
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'
