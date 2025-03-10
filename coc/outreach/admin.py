from django.contrib import admin

from .models import CharityCampaign, Donation, CharityEvent, EventRegistration
from .models import (DiscipleshipTrack, DiscipleshipModule, DiscipleshipLesson,
                     MentorshipRelationship, DiscipleshipProgress, MentorshipMeeting)
from .models import (
    Hospital,
    Department,
    MinistryService,
    VisitSchedule,
    PatientRequest,
    HospitalVisitReport,
    HospitalVolunteer, EvangelismTool
)
from .models import Mission, Project, ProjectUpdate
from .models import (PrisonFacility, InmateProgram, VolunteerApplication, MinistryResource, PrisonVisitReport)
from .models import ServiceCategory, ServiceProject, ServiceHours, ServiceReflection


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'contact_phone', 'active']
    list_filter = ['active']
    search_fields = ['name', 'address', 'contact_person']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'active')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_phone', 'contact_email')
        }),
        ('Visiting Details', {
            'fields': ('visiting_hours', 'special_instructions')
        })
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital', 'floor']
    list_filter = ['hospital']
    search_fields = ['name', 'hospital__name']


@admin.register(MinistryService)
class MinistryServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'duration']
    list_filter = ['service_type']
    search_fields = ['title', 'description']


@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ['service', 'hospital', 'department', 'date', 'status']
    list_filter = ['status', 'hospital', 'service']
    search_fields = ['notes', 'hospital__name', 'service__title']
    date_hierarchy = 'date'
    filter_horizontal = ['volunteers']
    readonly_fields = ['created_at']


@admin.register(PatientRequest)
class PatientRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'department', 'service_requested', 'priority', 'status']
    list_filter = ['status', 'priority', 'department__hospital']
    search_fields = ['patient_name', 'room_number', 'special_notes']
    readonly_fields = ['created_at', 'completed_at']
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_name', 'room_number', 'department')
        }),
        ('Request Details', {
            'fields': ('service_requested', 'priority', 'special_notes', 'preferred_time')
        }),
        ('Status', {
            'fields': ('status', 'assigned_to')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'completed_at')
        })
    )


@admin.register(HospitalVisitReport)
class HospitalVisitReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'visit', 'submitted_by', 'date', 'patients_visited']
    list_filter = ['date', 'submitted_by']
    search_fields = ['title', 'prayer_requests', 'testimonies']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'visit', 'submitted_by', 'patients_visited')
        }),
        ('Report Details', {
            'fields': ('prayer_requests', 'testimonies', 'challenges', 'follow_up_needed')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        })
    )


@admin.register(HospitalVolunteer)
class HospitalVolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'orientation_completed', 'created_at']
    list_filter = ['status', 'orientation_completed', 'hospitals']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    filter_horizontal = ['hospitals', 'services']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Volunteer Information', {
            'fields': ('user', 'status', 'orientation_completed')
        }),
        ('Assignments', {
            'fields': ('hospitals', 'services')
        }),
        ('Contact Information', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('Additional Details', {
            'fields': ('availability', 'medical_training')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        })
    )


@admin.register(PrisonVisitReport)
class PrisonVisitReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'visit', 'submitted_by', 'date', 'inmates_attended']
    list_filter = ['date', 'submitted_by']
    search_fields = ['title', 'activities_conducted', 'prayer_requests']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'visit', 'submitted_by', 'inmates_attended')
        }),
        ('Report Details', {
            'fields': ('activities_conducted', 'prayer_requests', 'testimonies',
                       'challenges', 'follow_up_needed', 'resources_used')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PrisonFacility)
class PrisonFacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'contact_phone', 'active']
    list_filter = ['active']
    search_fields = ['name', 'address', 'contact_person']


@admin.register(InmateProgram)
class InmateProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'facility', 'program_type', 'schedule', 'active']
    list_filter = ['program_type', 'active', 'facility']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'facility', 'status', 'created_at']
    list_filter = ['status', 'facility', 'background_check_consent']
    search_fields = ['user__username', 'user__email', 'experience']
    date_hierarchy = 'created_at'


@admin.register(MinistryResource)
class MinistryResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'quantity', 'facility']
    list_filter = ['resource_type', 'facility']
    search_fields = ['title', 'description']


@admin.register(DiscipleshipTrack)
class DiscipleshipTrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration_weeks', 'is_active']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


class DiscipleshipLessonInline(admin.StackedInline):
    model = DiscipleshipLesson
    extra = 1


@admin.register(DiscipleshipModule)
class DiscipleshipModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'track', 'order', 'estimated_hours']
    list_filter = ['track']
    search_fields = ['title', 'description']
    inlines = [DiscipleshipLessonInline]


@admin.register(MentorshipRelationship)
class MentorshipRelationshipAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'mentee', 'track', 'status', 'start_date']
    list_filter = ['status', 'track', 'start_date']
    search_fields = ['mentor__username', 'mentee__username']
    date_hierarchy = 'start_date'


@admin.register(DiscipleshipProgress)
class DiscipleshipProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'completion_date']
    list_filter = ['completed', 'completion_date']
    search_fields = ['user__username', 'lesson__title']


@admin.register(MentorshipMeeting)
class MentorshipMeetingAdmin(admin.ModelAdmin):
    list_display = ['relationship', 'date', 'next_meeting_date']
    list_filter = ['date']
    search_fields = ['topics_discussed', 'action_items']
    date_hierarchy = 'date'


@admin.register(CharityCampaign)
class CharityCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'cause', 'target_amount', 'raised_amount', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'cause', 'start_date']
    search_fields = ['title', 'description', 'beneficiary']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['raised_amount', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'cause', 'status')
        }),
        ('Financial Details', {
            'fields': ('target_amount', 'raised_amount')
        }),
        ('Campaign Period', {
            'fields': ('start_date', 'end_date')
        }),
        ('Contact Information', {
            'fields': ('beneficiary', 'contact_person', 'contact_email')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'campaign', 'amount', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'created_at', 'anonymous']
    search_fields = ['donor__username', 'campaign__title', 'message']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Donation Details', {
            'fields': ('campaign', 'donor', 'amount', 'message')
        }),
        ('Status', {
            'fields': ('payment_status', 'transaction_id', 'anonymous')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )


@admin.register(CharityEvent)
class CharityEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'campaign', 'date', 'location', 'current_participants', 'max_participants']
    list_filter = ['date', 'campaign']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['current_participants', 'created_at']
    fieldsets = (
        ('Event Information', {
            'fields': ('campaign', 'title', 'description', 'date', 'location')
        }),
        ('Capacity', {
            'fields': ('max_participants', 'current_participants')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['participant', 'event', 'registration_date', 'attended']
    list_filter = ['attended', 'registration_date']
    search_fields = ['participant__username', 'event__title']
    readonly_fields = ['registration_date']
    fieldsets = (
        ('Registration Details', {
            'fields': ('event', 'participant', 'attended')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('registration_date',)
        }),
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']


@admin.register(ServiceProject)
class ServiceProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'organization', 'start_date', 'status']
    list_filter = ['status', 'category', 'start_date']
    search_fields = ['title', 'description', 'organization']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'


@admin.register(ServiceHours)
class ServiceHoursAdmin(admin.ModelAdmin):
    list_display = ['student', 'project', 'date', 'hours', 'verified_by']
    list_filter = ['date', 'verified_by']
    search_fields = ['student__username', 'project__title', 'description']
    date_hierarchy = 'date'


@admin.register(ServiceReflection)
class ServiceReflectionAdmin(admin.ModelAdmin):
    list_display = ['student', 'project', 'created_at']
    list_filter = ['created_at']
    search_fields = ['student__username', 'project__title', 'reflection']
    date_hierarchy = 'created_at'



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


admin.site.register(EvangelismTool)
