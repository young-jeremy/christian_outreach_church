from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import *


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


admin.site.register(Resource)
admin.site.register(BibleStudyMaterial)
admin.site.register(DailyDevotion)
