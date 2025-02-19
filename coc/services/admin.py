from django.contrib import admin
from .models import (
    WorshipService, ForumCategory, ForumTopic, ForumPost, Topic, Post,
    BibleStudy, ChildRegistration, Testimony, ChildrenMinistry,
    NotificationPreferences, PrayerRequest, PrayerUpdate, SmallGroup,
    YouthEvent, YouthMinistry, ChildrenProgram, SongRequest, Event,
    EventRegistration, EventFeedback, Ministry, VolunteerOpportunity,
    VolunteerSignup, Child, MinistryRegistration, SermonCategory,
    SermonSeries, Sermon, SermonTag, SermonComment, SermonNote,
    Channel, Subscription, Notification, MarriageMinistry, CoupleProfile,
    MarriageEnrollment, MarriageResource, MarriageCounseling, MarriageEvent,
    FamilyGroup, FamilyEvent, ParentingResource, FamilyCounseling,
    FamilyDiscussion, DiscussionComment, NewBelieverProfile, DiscipleshipTrack,
    DiscipleshipModule, BelieverProgress, MentorshipSession, PrayerJournal,
    BibleReadingPlan, BibleReading, ReadingProgress, CoupleEvent,
    CounselingSession, CoupleResource, CoupleJournal, DateNightIdea,
    CouplePrayerRequest, WatchedVideo, DownloadedVideo, Category,
    CounselingRequest, WomensMinistry, MinistryEvent
)







@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'category', 'status', 'created_at')
    list_filter = ('category', 'status', 'is_anonymous')
    search_fields = ('title', 'request')

@admin.register(SmallGroup)
class SmallGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'meeting_frequency', 'is_accepting_members')
    list_filter = ('group_type', 'meeting_frequency', 'is_accepting_members')
    search_fields = ('name', 'description')

# Register remaining models with list displays
@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'is_featured')
    list_filter = ('is_featured', 'preacher')
    search_fields = ('title', 'description')

# Add more custom admin classes as needed for other models...

# Worship Service
@admin.register(WorshipService)
class WorshipServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'date', 'status', 'worship_leader')
    list_filter = ('service_type', 'status', 'is_online')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

# Forum
@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'created_at')
    list_filter = ('category', 'is_pinned', 'is_locked')
    search_fields = ('title', 'content')


# Bible Study
@admin.register(BibleStudy)
class BibleStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'study_type', 'start_date', 'is_online')
    list_filter = ('study_type', 'target_group', 'is_online')
    search_fields = ('title', 'description')

# Marriage Ministry
@admin.register(MarriageMinistry)
class MarriageMinistryAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'meeting_type')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(CoupleProfile)
class CoupleProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'partner_name', 'marriage_stage', 'anniversary')
    list_filter = ('marriage_stage', 'is_public')
    search_fields = ('user__username', 'partner_name')

#
@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

# Register remaining models with basic ModelAdmin
admin.site.register(Post)
admin.site.register(ChildRegistration)
admin.site.register(Testimony)
admin.site.register(ChildrenMinistry)
admin.site.register(NotificationPreferences)
admin.site.register(PrayerUpdate)
admin.site.register(Child)
admin.site.register(MinistryRegistration)
admin.site.register(SermonCategory)
admin.site.register(SermonTag)
admin.site.register(SermonComment)
admin.site.register(SermonNote)
admin.site.register(Channel)
admin.site.register(Subscription)
admin.site.register(Notification)
admin.site.register(MarriageEnrollment)
admin.site.register(MarriageResource)
admin.site.register(MarriageCounseling)
admin.site.register(MarriageEvent)
admin.site.register(FamilyGroup)
admin.site.register(FamilyCounseling)
admin.site.register(FamilyDiscussion)
admin.site.register(DiscussionComment)
admin.site.register(NewBelieverProfile)
admin.site.register(DiscipleshipTrack)
admin.site.register(DiscipleshipModule)
admin.site.register(BelieverProgress)
admin.site.register(MentorshipSession)
admin.site.register(PrayerJournal)
admin.site.register(BibleReadingPlan)
admin.site.register(BibleReading)
admin.site.register(ReadingProgress)
admin.site.register(CoupleEvent)
admin.site.register(CounselingSession)
admin.site.register(CoupleResource)
admin.site.register(CoupleJournal)
admin.site.register(DateNightIdea)
admin.site.register(CouplePrayerRequest)
admin.site.register(WatchedVideo)
admin.site.register(DownloadedVideo)
admin.site.register(Category)
admin.site.register(VolunteerOpportunity)
admin.site.register(YouthEvent)
admin.site.register(CounselingRequest)
admin.site.register(WomensMinistry)
admin.site.register(MinistryEvent)
