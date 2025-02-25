from django.contrib import admin
from .models import (
    Content, ContentGuidelines, Moderation, ModerationRequest, FavoriteVideo, Advertisement, WatchedVideo, Category

)
from django.contrib import messages
from django.utils.translation import ngettext

from .models import (
    Content, ContentGuidelines, Moderation, ModerationRequest, FavoriteVideo, Advertisement, WatchedVideo, Category

)
from .models import ShortVideo, Privacy, LikedVideo, UploadedVideo, VideoView, Share, Comments, VideoLikes, WatchLater, \
    Playlist
from .models import Video, Comment


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'view_count', 'created_at', 'is_active']
    list_filter = ['category', 'is_active', 'is_featured', 'has_profanity']
    search_fields = ['title', 'description', 'user__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['view_count', 'like_count', 'comment_count', 'processing_status']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'video_file', 'thumbnail')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Settings', {
            'fields': ('visibility', 'language', 'is_active', 'is_featured')
        }),
        ('Processing', {
            'fields': ('processing_status', 'has_profanity', 'captions')
        }),
        ('Statistics', {
            'fields': ('view_count', 'like_count', 'comment_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('user', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['text', 'user__username', 'video__title']
    readonly_fields = ['like_count']


@admin.register(ContentGuidelines)
class ContentGuidelineAdmin(admin.ModelAdmin):
    list_display = ['title']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'description', 'uploader', 'status', 'privacy', 'category', 'path',]

    actions = ['make_published', 'make_blocked', 'make_pending']

    @admin.action(description='Mark the SELECTED videos as APPROVED')
    def make_published(self, request, queryset):
        updated = queryset.update(status='APPROVED')
        self.message_user(request, ngettext(
            '%d video was successfully marked as published',
            '%d videos were successfully marked as published',
            updated,



        )
                  % updated, messages.SUCCESS
                          )

    @admin.action(description='Mark selected videos as BLOCKED')
    def make_blocked(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, ngettext(
            '%d video was successfully marked as blocked',
            '%d videos were successfully marked as blocked',
            updated,



        )
                  % updated, messages.SUCCESS
                          )

    @admin.action(description='Mark selected videos as PENDING')
    def make_pending(self, request, queryset):
        updated = queryset.update(status='PENDING')
        self.message_user(request, ngettext(
            '%d video was successfully marked as pending',
            '%d video were successfully marked as pending',
            updated,



        )
                  % updated, messages.SUCCESS
                          )


admin.site.register(Content, ContentAdmin)
admin.site.register(Moderation)
admin.site.register(Playlist)
admin.site.register(ModerationRequest)
admin.site.register(LikedVideo)
admin.site.register(FavoriteVideo)
admin.site.register(Advertisement)
admin.site.register(WatchedVideo)
admin.site.register(WatchLater)
admin.site.register(Category)
admin.site.register(ShortVideo)
admin.site.register(Privacy)
admin.site.register(UploadedVideo)
admin.site.register(VideoView)
admin.site.register(Share)
admin.site.register(Comments)
admin.site.register(VideoLikes)
