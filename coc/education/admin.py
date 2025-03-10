from django.contrib import admin
from django.utils.html import format_html

from .models import (
    BibleCollegeProgram, BibleCollegeCourse, BibleCollegeStudent,
    BibleCollegeEnrollment, BibleCollegeAssignment, BibleCollegeSubmission,
    BibleCollegeFaculty
)
from .models import (BiblicalCourse, CourseModule, Lesson, Assignment,
                     StudentEnrollment, AssignmentSubmission, Discussion,
                     DiscussionReply)
from .models import (
    Bibliography
)
from .models import (
    ChristianMentorProfile,
    ChristianMentorshipSession,
    ChristianMentorshipApplication,
    ChristianMentorshipFeedback
)
from .models import (
    LeadershipTraining, TrainingModule, TrainingSession,
    LeadershipAssessment, ParticipantEnrollment, AssessmentSubmission,
    MentorshipSession
)
from .models import (
    SundaySchoolMaterial, AgeGroup, Activity, TeachingResource, Feedback,
    TheologicalResource, TheologicalCategory, StudyNote, ResourceReview
)


@admin.register(BibleCollegeProgram)
class BibleCollegeProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'duration_years', 'credits_required', 'is_active']
    list_filter = ['level', 'is_active']
    search_fields = ['name', 'description']


@admin.register(BibleCollegeCourse)
class BibleCollegeCourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'program', 'credits', 'semester', 'year_level']
    list_filter = ['program', 'semester', 'year_level']
    search_fields = ['code', 'title', 'description']
    filter_horizontal = ['prerequisites']


@admin.register(BibleCollegeStudent)
class BibleCollegeStudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'program', 'enrollment_date', 'current_year']
    list_filter = ['program', 'current_year']
    search_fields = ['user__username', 'user__email', 'testimony']
    raw_id_fields = ['user']


@admin.register(BibleCollegeEnrollment)
class BibleCollegeEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'year', 'completed', 'grade']
    list_filter = ['semester', 'year', 'completed']
    search_fields = ['student__user__username', 'course__code']
    raw_id_fields = ['student', 'course']


@admin.register(BibleCollegeAssignment)
class BibleCollegeAssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'total_marks', 'weight_percentage']
    list_filter = ['course', 'due_date']
    search_fields = ['title', 'description', 'course__code']
    date_hierarchy = 'due_date'


@admin.register(BibleCollegeSubmission)
class BibleCollegeSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'assignment', 'submission_date',
        'marks_obtained', 'get_percentage'
    ]
    list_filter = ['submission_date', 'assignment__course']
    search_fields = ['student__user__username', 'assignment__title']
    raw_id_fields = ['student', 'assignment']
    date_hierarchy = 'submission_date'

    def get_percentage(self, obj):
        if obj.marks_obtained and obj.assignment.total_marks:
            return f"{(obj.marks_obtained / obj.assignment.total_marks) * 100:.1f}%"
        return "N/A"

    get_percentage.short_description = "Percentage"


@admin.register(BibleCollegeFaculty)
class BibleCollegeFacultyAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'get_courses']
    search_fields = ['user__username', 'user__email', 'title', 'qualifications']
    raw_id_fields = ['user']
    filter_horizontal = ['courses']

    def get_courses(self, obj):
        return ", ".join([course.code for course in obj.courses.all()])

    get_courses.short_description = "Courses"


@admin.register(ChristianMentorProfile)
class ChristianMentorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'ministry_focus', 'years_in_ministry', 'accepting_mentees']
    list_filter = ['accepting_mentees', 'years_in_ministry']
    search_fields = ['user__username', 'user__email', 'ministry_focus']


@admin.register(ChristianMentorshipSession)
class ChristianMentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'mentor', 'scripture_focus', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['topic', 'scripture_focus', 'description']
    filter_horizontal = ['participants']


@admin.register(ChristianMentorshipApplication)
class ChristianMentorshipApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'mentor', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['applicant__username', 'mentor__user__username']


@admin.register(ChristianMentorshipFeedback)
class ChristianMentorshipFeedbackAdmin(admin.ModelAdmin):
    list_display = ['session', 'participant', 'spiritual_growth_rating', 'created_at']
    list_filter = ['spiritual_growth_rating', 'mentorship_quality', 'created_at']
    search_fields = ['session__topic', 'participant__username']


@admin.register(TheologicalCategory)
class TheologicalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(TheologicalResource)
class TheologicalResourceAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'resource_type',
        'level', 'download_count', 'is_featured', 'is_public'
    )
    list_filter = (
        'category', 'resource_type', 'level',
        'is_featured', 'is_public', 'requires_permission'
    )
    search_fields = ('title', 'author', 'description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('download_count', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'author', 'category',
                'resource_type', 'level', 'description'
            )
        }),
        ('Content', {
            'fields': (
                'content', 'scripture_references',
                'key_points', 'publication_date'
            )
        }),
        ('Files and Links', {
            'fields': ('file', 'external_link', 'thumbnail')
        }),
        ('Settings', {
            'fields': (
                'is_featured', 'is_public', 'requires_permission',
                'download_count', 'created_at', 'updated_at'
            )
        }),
    )


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource', 'user', 'is_private', 'created_at')
    list_filter = ('is_private', 'created_at')
    search_fields = ('title', 'content', 'user__username', 'resource__title')
    date_hierarchy = 'created_at'


@admin.register(ResourceReview)
class ResourceReviewAdmin(admin.ModelAdmin):
    list_display = (
        'resource', 'user', 'rating', 'theological_accuracy',
        'clarity', 'practicality', 'is_approved'
    )
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('review_text', 'user__username', 'resource__title')
    date_hierarchy = 'created_at'
    actions = ['approve_reviews', 'unapprove_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = "Approve selected reviews"

    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)

    unapprove_reviews.short_description = "Unapprove selected reviews"


@admin.register(Bibliography)
class BibliographyAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'resource', 'year', 'publication')
    list_filter = ('year', 'resource')
    search_fields = ('title', 'authors', 'publication', 'resource__title')


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'age_range')
    search_fields = ('name', 'age_range')


@admin.register(SundaySchoolMaterial)
class SundaySchoolMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'age_group', 'category', 'created_by', 'is_active')
    list_filter = ('age_group', 'category', 'is_active')
    search_fields = ('title', 'description', 'bible_reference')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'material', 'duration_minutes', 'order')
    list_filter = ('material__age_group',)
    search_fields = ('title', 'description')
    ordering = ('material', 'order')


@admin.register(TeachingResource)
class TeachingResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'material', 'resource_type', 'is_downloadable')
    list_filter = ('resource_type', 'is_downloadable')
    search_fields = ('title', 'description')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('material', 'teacher', 'rating', 'used_date')
    list_filter = ('rating', 'used_date')
    search_fields = ('material__title', 'teacher__username', 'comment')
    date_hierarchy = 'created_at'


@admin.register(LeadershipTraining)
class LeadershipTrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'mentor', 'duration_weeks', 'is_active')
    list_filter = ('category', 'level', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'training', 'order')
    list_filter = ('training',)
    search_fields = ('title', 'description')
    ordering = ('training', 'order')


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'duration_minutes', 'order')
    list_filter = ('module__training',)
    search_fields = ('title', 'content')
    ordering = ('module', 'order')


@admin.register(LeadershipAssessment)
class LeadershipAssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'assessment_type', 'passing_score')
    list_filter = ('assessment_type', 'session__module__training')
    search_fields = ('title', 'description', 'criteria')


@admin.register(ParticipantEnrollment)
class ParticipantEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('participant', 'training', 'status', 'enrolled_date', 'completion_date')
    list_filter = ('status', 'training')
    search_fields = ('participant__email', 'participant__first_name', 'participant__last_name')
    raw_id_fields = ('participant', 'approved_by')
    date_hierarchy = 'enrolled_date'


@admin.register(AssessmentSubmission)
class AssessmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('participant', 'assessment', 'status', 'score', 'submitted_date')
    list_filter = ('status', 'assessment__assessment_type')
    search_fields = ('participant__email', 'submission_text')
    raw_id_fields = ('participant', 'reviewed_by')
    date_hierarchy = 'submitted_date'


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'participant', 'training', 'scheduled_date', 'completed')
    list_filter = ('completed', 'training')
    search_fields = ('mentor__email', 'participant__email', 'topics')
    raw_id_fields = ('mentor', 'participant')
    date_hierarchy = 'scheduled_date'


@admin.register(BiblicalCourse)
class BiblicalCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration_weeks', 'is_active', 'created_at', 'show_image']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50"/>', obj.image.url)
        return "No Image"

    show_image.short_description = 'Course Image'


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'description']
    ordering = ['course', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'duration_minutes']
    list_filter = ['module__course', 'module']
    search_fields = ['title', 'content']
    ordering = ['module', 'order']
    autocomplete_fields = ['module']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'due_days', 'points']
    list_filter = ['lesson__module__course']
    search_fields = ['title', 'description']
    autocomplete_fields = ['lesson']


# ... (previous imports and other admin classes remain the same)

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_date', 'status']
    list_filter = ['status', 'enrolled_date', 'course']
    search_fields = ['student__username', 'student__email', 'course__title']
    readonly_fields = ['enrolled_date']
    date_hierarchy = 'enrolled_date'


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_date', 'status', 'grade']
    list_filter = ['status', 'submitted_date', 'assignment__lesson__module__course']
    search_fields = ['student__username', 'student__email', 'assignment__title']
    readonly_fields = ['submitted_date']
    date_hierarchy = 'submitted_date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(assignment__lesson__module__course__created_by=request.user)
        return qs


# ... (rest of the file remains the same)

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'created_by', 'created_at']
    list_filter = ['lesson__module__course', 'created_at']
    search_fields = ['title', 'content', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ['discussion', 'created_by', 'created_at']
    list_filter = ['discussion__lesson__module__course', 'created_at']
    search_fields = ['content', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


# Custom admin site configuration
admin.site.site_header = 'Biblical Education Administration'
admin.site.site_title = 'Biblical Education Admin Portal'
admin.site.index_title = 'Welcome to Biblical Education Administration'


# Optional: Add custom admin actions
@admin.action(description='Mark selected courses as active')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Mark selected courses as inactive')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


# Add these actions to the BiblicalCourseAdmin
BiblicalCourseAdmin.actions = [make_active, make_inactive]
