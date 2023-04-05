from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_on', 'last_update')
    list_filter = ('title', 'author', 'category', 'created_on', 'last_update')
    search_fields = ('title', 'slug', 'author', 'main_text', 'category', 'tag')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'comment_text')
    actions = ['approve_comments']

    @staticmethod
    def approve_comments(request, queryset):
        queryset.update(active=True)


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'bio', 'address', 'created_on')
    list_filter = ('user', 'address', 'created_on')
    search_fields = ('user', 'bio', 'created_on')
    readonly_fields = ('id', 'created_on')
