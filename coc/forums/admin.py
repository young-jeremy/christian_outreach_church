from django.contrib import admin
from .models import ForumCategory, Topic, Post, Notification

@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic_count', 'post_count', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'created_at', 'views')
    list_filter = ('category', 'created_at', 'is_pinned', 'is_locked')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at', 'is_solution')
    list_filter = ('created_at', 'is_solution')
    search_fields = ('content',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'created_at', 'is_read')
    list_filter = ('notification_type', 'is_read', 'created_at') 