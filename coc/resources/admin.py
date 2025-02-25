from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *


@admin.register(SermonNotes)
class SermonNotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'category', 'is_featured')
    list_filter = ('category', 'date_preached', 'preacher', 'is_featured')
    search_fields = ('title', 'preacher', 'bible_reference', 'main_points', 'summary')
    date_hierarchy = 'date_preached'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'preacher', 'date_preached', 'category', 'bible_reference')
        }),
        ('Sermon Content', {
            'fields': ('main_points', 'key_scriptures', 'summary', 'application_points', 'additional_notes')
        }),
        ('Resources', {
            'fields': ('audio_recording', 'slides')
        }),
        ('Settings', {
            'fields': ('is_featured', 'created_at', 'updated_at')
        }),
    )

class ReviewInline(GenericTabularInline):
    model = ReviewableMixin
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_active', 'featured']
    list_filter = ['category', 'is_active', 'featured']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'category', 'description')
        }),
        ('Publication Details', {
            'fields': ('publisher', 'publication_date', 'isbn')
        }),
        ('Files', {
            'fields': ('cover_image', 'pdf_file', 'sample_chapter')
        }),
        ('Settings', {
            'fields': ('is_active', 'featured', 'added_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DownloadableResource)
class DownloadableResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'category', 'download_count', 'is_public', 'featured')
    list_filter = ('resource_type', 'category', 'is_public', 'requires_login', 'featured')
    search_fields = ('title', 'description', 'tags')
    readonly_fields = ('file_size', 'file_type', 'download_count', 'last_downloaded')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'author', 'version')
        }),
        ('File', {
            'fields': ('file', 'thumbnail', 'resource_type', 'category')
        }),
        ('Access Control', {
            'fields': ('is_public', 'requires_login', 'allowed_groups')
        }),
        ('Organization', {
            'fields': ('tags', 'featured')
        }),
        ('File Information', {
            'fields': ('file_size', 'file_type'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('download_count', 'last_downloaded'),
            'classes': ('collapse',)
        })
    )


admin.site.register(Resource)
admin.site.register(BibleStudyMaterial)
admin.site.register(DailyDevotion)
admin.site.register(Podcast)
admin.site.register(TeachingResource)
