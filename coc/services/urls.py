from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Core URLs
    path('', views.services, name='services_home'),
    path('subscriptions/', views.subscriptions_view, name='subscriptions'),
    path('subscribe/<int:channel_id>/', views.subscribe_view, name='subscribe'),
    path('unsubscribe/<int:channel_id>/', views.unsubscribe_view, name='unsubscribe'),
    # Add this to your existing urlpatterns
    path('worship-services/song-request/', views.submit_song_request, name='submit_song_request'),

    # Sermon URLs
    path('sermons/', views.sermon_list, name='sermon_list'),
    path('sermons/<slug:sermon_slug>/', views.sermon_detail, name='sermon_details'),  # Fixed duplicate slug
    path('sermons/<slug:sermon_slug>/like/', views.like_sermon, name='like_sermon'),
    path('sermons/<slug:sermon_slug>/note/', views.save_note, name='save_note'),
    path('sermons/add/', views.add_sermon, name='add_sermon'),
    # Category URLs
    path('categories/', views.sermon_categories, name='categories'),
    path('categories/<slug:category_slug>/edit/', views.edit_sermon_category, name='edit_category'),
    path('categories/<slug:category_slug>/delete/', views.delete_sermon_category, name='delete_category'),

    # Bible Study URLs
    path('bible-studies/', views.bible_study_list, name='bible_study_list'),
    path('bible-studies/<int:pk>/', views.bible_study_detail, name='bible_study_detail'),
    path('bible-studies/create/', views.create_bible_study, name='create_bible_study'),
    path('events/', views.events_view, name='events_view'),

    # Worship Service URLs
    path('worship-services/', views.worship_service_list, name='worship_service_list'),
    path('worship-services/create/', views.create_worship_service, name='create_worship_service'),

    # Youth Ministry URLs
    path('youth/', views.youth_ministry_list, name='youth_ministry_list'),
    path('youth/<int:pk>/', views.youth_event_detail, name='youth_event_detail'),
    path('youth/create/', views.create_youth_event, name='create_youth_event'),
    path('youth/events/', views.youth_events_list, name='youth_events_list'),

    # Children's Ministry URLs
    path('children/', views.children_ministry_list, name='children_ministry_list'),

    path('children/register/', views.register_child, name='register_child'),
    path('ministries/children/create/', views.create_children_program, name='create_children_program'),

    # Testimony URLs
    path('testimonies/', views.testimony_list, name='testimony_list'),
    path('testimonies/create/', views.create_testimony, name='create_testimony'),
    path('testimonies/<int:pk>/', views.testimony_detail, name='testimony_detail'),
    path('testimonies/<int:pk>/approve/', views.approve_testimony, name='approve_testimony'),
    path('add_testimony/<int:pk>/', views.add_testimony, name='add_testimony'),

    path('prayer-requests/', views.prayer_requests_list, name='prayer_requests'),
    path('prayer-requests/create/', views.create_prayer_request, name='create_prayer_request'),
    path('prayer-requests/<int:pk>/', views.prayer_request_detail, name='prayer_request_detail'),
    path('prayer-requests/<int:pk>/update/', views.add_prayer_update, name='add_prayer_update'),
    path('prayer-requests/<int:pk>/pray/', views.toggle_prayer_warrior, name='toggle_prayer_warrior'),

    path('small-groups/', views.small_groups_list, name='small_groups'),
    path('small-groups/create/', views.create_small_group, name='create_small_group'),
    path('small-groups/<int:pk>/', views.small_group_detail, name='small_group_detail'),
    path('small-groups/<int:pk>/join/', views.join_small_group, name='join_small_group'),
    path('small-groups/<int:pk>/', views.small_group_detail, name='small_group_detail'),
    path('small-groups/<int:pk>/leave/', views.leave_small_group, name='leave_small_group'),

    # Forums URLs - Move these BEFORE the opportunity URLs
    path('fellowship_forums/', views.ForumListView.as_view(), name='fellowship_forums'),
    path('fellowship_forums/category/<slug:category_slug>/', views.ForumCategoryView.as_view(), name='forum_category'),
    path('fellowship_forums/topic/<slug:slug>/', views.ForumTopicView.as_view(), name='forum_topic'),
    path('fellowship_forums/create/', views.CreateForumTopicView.as_view(), name='create_forum_topic'),

    # Opportunity URLs - Keep these after the forums URLs
    path('opportunity_list/', views.OpportunityListView.as_view(), name='opportunity_list'),
    path('opportunity/create/', views.OpportunityCreateView.as_view(), name='create_opportunity'),
    path('opportunity/<slug:slug>/', views.OpportunityDetailView.as_view(), name='opportunity_detail'),
    path('opportunity/<slug:slug>/edit/', views.OpportunityUpdateView.as_view(), name='edit_opportunity'),
    path('opportunity/<slug:slug>/delete/', views.OpportunityDeleteView.as_view(), name='delete_opportunity'),
    path('opportunity/<slug:slug>/signup/', views.volunteer_signup, name='signup'),
    path('opportunity/<slug:slug>/cancel/', views.cancel_signup, name='cancel_signup'),

    # forums
    path('fellowship_forums/', views.ForumHomeView.as_view(), name='fellowship_forums'),
    path('category/<slug:category_slug>/', views.TopicListView.as_view(), name='topic_list'),
    path('topic/<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('create-topic/', views.CreateTopicView.as_view(), name='create_topic'),
    path('topic/<slug:topic_slug>/reply/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    # ... your existing URLs ...
    path('fellowship_forums/', views.ForumListView.as_view(), name='forum_list'),
    path('fellowship_forums/category/<slug:category_slug>/', views.ForumCategoryView.as_view(), name='forum_category'),
    path('fellowship_forums/topic/<slug:slug>/', views.ForumTopicView.as_view(), name='forum_topic'),
    path('fellowship_forums/create/', views.CreateForumTopicView.as_view(), name='create_forum_topic'),

    # Marriage Ministry URLs
    path('marriage/', views.MarriageMinistryListView.as_view(), name='marriage_list'),
    path('marriage/<slug:slug>/', views.MarriageMinistryDetailView.as_view(), name='marriage_detail'),
    path('marriage/create/', views.MarriageMinistryCreateView.as_view(), name='marriage_create'),
    path('marriage/couple-profile/create/', views.create_couple_profile, name='couple_profile_create'),
    path('marriage/resources/', views.MarriageResourceListView.as_view(), name='marriage_resources'),
    path('marriage/counseling/request/', views.MarriageCounselingCreateView.as_view(), name='counseling_request'),
    path('marriage/events/', views.MarriageEventListView.as_view(), name='marriage_events'),

    # Family Life URLs
    path('family/', views.FamilyLifeHomeView.as_view(), name='family_home'),
    path('family/events/', views.FamilyEventListView.as_view(), name='family_events'),
    path('family/resources/', views.ParentingResourceListView.as_view(), name='family_resources'),
    path('family/discussions/', views.FamilyDiscussionListView.as_view(), name='family_discussions'),
    path('family/discussions/<slug:slug>/', views.FamilyDiscussionDetailView.as_view(),
         name='family_discussion_detail'),
    path('family/counseling/request/', views.FamilyCounselingCreateView.as_view(), name='family_counseling_request'),
    path('family/discussions/create/', views.FamilyDiscussionCreateView.as_view(), name='family_discussion_create'),
    path('family/discussions/<slug:slug>/like/', views.family_discussion_like, name='family_discussion_like'),
    path('family/discussions/<slug:slug>/comment/', views.family_discussion_comment, name='family_discussion_comment'),
    # Add this to your family life URLs
    path('family/events/create/', views.FamilyEventCreateView.as_view(), name='family_event_create'),
    path('family/resources/create/', views.FamilyResourceCreateView.as_view(), name='family_resource_create'),

    # New Believers URLs
    path('new-believers/', views.NewBelieversDashboard.as_view(), name='new_believers_dashboard'),
    path('new-believers/profile/', views.NewBelieverProfileView.as_view(), name='believer_profile'),
    path('new-believers/profile/create/', views.NewBelieverProfileCreate.as_view(), name='create_believer_profile'),
    path('new-believers/discipleship/', views.DiscipleshipTrackList.as_view(), name='discipleship_tracks'),
    path('new-believers/discipleship/<slug:slug>/', views.DiscipleshipTrackDetail.as_view(), name='track_detail'),
    path('new-believers/mentorship/', views.MentorshipSessionList.as_view(), name='mentorship_sessions'),
    path('new-believers/mentorship/schedule/', views.ScheduleMentorshipSession.as_view(), name='schedule_session'),
    path('new-believers/prayer-journal/', views.PrayerJournalList.as_view(), name='prayer_journal'),
    path('new-believers/bible-reading/', views.BibleReadingPlanList.as_view(), name='bible_reading_plans'),
    path('new-believers/bible-reading/<slug:slug>/', views.BibleReadingPlanDetail.as_view(),
         name='reading_plan_detail'),
    path('new-believers/reading/<slug:plan_slug>/complete/<int:day_number>/', views.complete_reading,
         name='complete_reading'),
    path('new-believers/prayer-journal/add/', views.add_prayer_entry, name='add_prayer_entry'),
    path('new-believers/prayer-journal/<int:pk>/update/', views.update_prayer_status, name='update_prayer_status'),
    path('new-believers/discipleship/<slug:track_slug>/complete/<int:module_id>/', views.complete_module,
         name='complete_module'),
    path('new-believers/mentorship/<int:session_id>/complete/', views.complete_mentorship_session,
         name='complete_session'),
    path('new-believers/profile/baptism/', views.update_baptism_status, name='update_baptism'),

    # Couples Ministry URLs
    path('couples/', views.CouplesHomeView.as_view(), name='couples_home'),
    path('couples/profile/', views.CoupleProfileView.as_view(), name='couple_profile'),
    path('couples/events/', views.CoupleEventList.as_view(), name='couple_events'),
    path('couples/events/<slug:slug>/', views.CoupleEventDetail.as_view(), name='event_detail'),
    path('couples/events/<slug:slug>/register/', views.event_registration, name='event_registration'),
    path('couples/counseling/', views.CounselingSessionList.as_view(), name='counseling_sessions'),
    path('couples/counseling/schedule/', views.ScheduleCounseling.as_view(), name='schedule_counseling'),
    path('couples/resources/', views.CoupleResourceList.as_view(), name='couple_resources'),
    path('couples/journal/', views.CoupleJournalList.as_view(), name='couple_journal'),
    path('couples/journal/add/', views.add_journal_entry, name='add_journal_entry'),
    path('couples/prayer/', views.PrayerRequestList.as_view(), name='couple_prayers'),
    path('couples/date-ideas/', views.DateNightIdeaList.as_view(), name='date_ideas'),
    path('couples/reading-plans/', views.couple_reading_plans, name='couple_reading_plans'),
 # Bible Reading Plans
    path('couples/reading-plans/create/', views.create_reading_plan, name='create_reading_plan'),  # Add this line
    path('couples/reading-plans/<int:pk>/', views.reading_plan_detail, name='reading_plan_detail'),

    # Add these to your existing urlpatterns
    path('womens-ministry/', views.womens_ministry_list, name='womens_ministry_list'),
    path('womens-ministry/create/', views.womens_ministry_create, name='womens_ministry_create'),
    path('womens-ministry/<slug:slug>/', views.womens_ministry_detail, name='womens_ministry_detail'),
    path('womens-ministry/<slug:ministry_slug>/event/create/', views.ministry_event_create,
             name='ministry_event_create'),
    path('womens-ministry/<int:ministry_id>/toggle-membership/', views.toggle_ministry_membership, name='toggle_ministry_membership'),
    path('ministry-event/<int:event_id>/toggle-attendance/', views.toggle_event_attendance, name='toggle_event_attendance'),
    # Add these to your existing urlpatterns
    path('mens-ministry/', views.mens_ministry_list, name='mens_ministry_list'),
    path('mens-ministry/create/', views.mens_ministry_create, name='mens_ministry_create'),
    path('mens-ministry/<slug:slug>/', views.mens_ministry_detail, name='mens_ministry_detail'),
    path('mens-ministry/<slug:ministry_slug>/event/create/', views.mens_event_create, name='mens_event_create'),
    path('mens-ministry/event/<int:event_id>/toggle-attendance/', views.toggle_event_attendance, name='mens_event_toggle_attendance'),






]