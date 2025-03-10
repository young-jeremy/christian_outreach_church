from django.contrib import admin
from django.utils.html import format_html

from .models import (
    PhotoAlbum,
    Photo,
    NewsArticle,
    Newsletter,
    Announcement,
    TestimonialVideo,
    AudioMessage
)
from .models import VideoCategory, ArchivedVideo, LiveStream


@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'photo_count')  # Removed is_featured
    list_filter = ('created_at',)  # Removed is_featured
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'album', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'album')
    search_fields = ('caption', 'album__title')
    date_hierarchy = 'uploaded_at'


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')  # Removed is_featured
    list_filter = ('published_date',)  # Removed is_featured
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'issue_number', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('title', 'description')
    date_hierarchy = 'publication_date'
    ordering = ('-issue_number',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'start_date', 'end_date', 'is_active', 'created_by')
    list_filter = ('priority', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'content')
    date_hierarchy = 'start_date'

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TestimonialVideo)
class TestimonialVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'person_name', 'uploaded_by', 'view_count')  # Removed is_featured
    list_filter = ('recorded_date', 'uploaded_at')  # Removed is_featured
    search_fields = ('title', 'person_name', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'recorded_date'


@admin.register(AudioMessage)
class AudioMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'category', 'recorded_date', 'duration')
    list_filter = ('category', 'recorded_date')
    search_fields = ('title', 'description', 'speaker__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'recorded_date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('speaker')


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'video_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

    def video_count(self, obj):
        return obj.videos.count()

    video_count.short_description = 'Number of Videos'


@admin.register(ArchivedVideo)
class ArchivedVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'upload_date', 'view_count',
                    'is_featured', 'thumbnail_preview', 'uploaded_by']
    list_filter = ['category', 'upload_date', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'upload_date', 'duration', 'thumbnail_preview']
    date_hierarchy = 'upload_date'
    list_per_page = 20

    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Media Files', {
            'fields': ('video_file', 'thumbnail', 'thumbnail_preview')
        }),
        ('Status', {
            'fields': ('is_featured', 'view_count', 'duration')
        }),
        ('Upload Details', {
            'fields': ('uploaded_by', 'upload_date'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.thumbnail.url
            )
        return "No thumbnail"

    thumbnail_preview.short_description = 'Thumbnail'

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ['title', 'scheduled_time', 'is_live', 'viewers_count',
                    'created_by', 'created_at']
    list_filter = ['is_live', 'created_at', 'scheduled_time']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['stream_key', 'viewers_count', 'created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Stream Information', {
            'fields': ('title', 'description', 'thumbnail')
        }),
        ('Stream Settings', {
            'fields': ('scheduled_time', 'is_live', 'stream_key')
        }),
        ('Statistics', {
            'fields': ('viewers_count', 'created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ('stream_key',)
        return self.readonly_fields


# Optional: Custom admin site configuration
admin.site.site_header = 'COC Media Administration'
admin.site.site_title = 'COC Media Admin Portal'
admin.site.index_title = 'Media Management'
