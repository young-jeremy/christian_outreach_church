from django.contrib import admin

from .models import Mission, Project, ProjectUpdate


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date', 'status', 'team_size')
    list_filter = ('status', 'start_date', 'location')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'status', 'featured_image')
        }),
        ('Location & Timing', {
            'fields': ('location', 'start_date', 'end_date')
        }),
        ('Resources', {
            'fields': ('budget', 'team_size', 'impact_summary')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'mission', 'category', 'status', 'project_lead', 'start_date')
    list_filter = ('status', 'category', 'mission', 'start_date')
    search_fields = ('title', 'description', 'project_lead', 'location')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'mission', 'category', 'status')
        }),
        ('Location & Timing', {
            'fields': ('location', 'start_date', 'end_date')
        }),
        ('Team & Contact', {
            'fields': ('project_lead', 'contact_email')
        }),
        ('Resources & Outcomes', {
            'fields': ('budget', 'goals', 'outcomes', 'featured_image')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'date', 'created_at')
    list_filter = ('project', 'date')
    search_fields = ('title', 'content', 'project__title')
    date_hierarchy = 'date'
    ordering = ('-date',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'content', 'image', 'date')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )
