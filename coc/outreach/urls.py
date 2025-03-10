from django.urls import path

from . import views

app_name = 'outreach'

urlpatterns = [
    # Mission URLs
    path('missions/', views.MissionListView.as_view(), name='mission_list'),
    path('missions/create/', views.MissionCreateView.as_view(), name='mission_create'),
    path('missions/<slug:slug>/', views.MissionDetailView.as_view(), name='mission_detail'),
    path('missions/<slug:slug>/edit/', views.MissionUpdateView.as_view(), name='mission_edit'),
    path('missions/<slug:slug>/delete/', views.MissionDeleteView.as_view(), name='mission_delete'),

    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<slug:slug>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # Project Update URLs
    path('projects/<int:project_id>/updates/create/',
         views.ProjectUpdateCreateView.as_view(), name='project_update_create'),
    path('projects/updates/<int:pk>/edit/',
         views.ProjectUpdateUpdateView.as_view(), name='project_update_edit'),
    path('projects/updates/<int:pk>/delete/',
         views.ProjectUpdateDeleteView.as_view(), name='project_update_delete'),

    # Add to your urlpatterns
    path('tools/', views.ToolListView.as_view(), name='tool_list'),
    path('tools/<slug:slug>/', views.ToolDetailView.as_view(), name='tool_detail'),
    path('tools/create/', views.ToolCreateView.as_view(), name='tool_create'),
    path('tools/<slug:slug>/edit/', views.ToolUpdateView.as_view(), name='tool_edit'),
    path('tools/<slug:slug>/download/', views.download_tool, name='tool_download'),

    # Add these URLs to your existing urls.py patterns

    path('service/', views.ServiceProjectListView.as_view(), name='service_project_list'),
    path('service/<slug:slug>/', views.ServiceProjectDetailView.as_view(), name='service_project_detail'),
    path('service/<slug:project_slug>/log-hours/', views.log_service_hours, name='log_service_hours'),
    path('service/<slug:project_slug>/reflect/', views.submit_reflection, name='submit_reflection'),
    path('service/dashboard/', views.service_dashboard, name='service_dashboard'),

    path('charity/', views.CharityCampaignListView.as_view(), name='campaign_list'),
    path('charity/<slug:slug>/', views.CharityCampaignDetailView.as_view(), name='campaign_detail'),
    path('charity/<slug:campaign_slug>/donate/', views.make_donation, name='make_donation'),
    path('charity/event/<int:event_id>/register/', views.register_for_event, name='register_event'),
    path('charity/dashboard/', views.charity_dashboard, name='charity_dashboard'),

    path('discipleship/', views.TrackListView.as_view(), name='track_list'),
    path('discipleship/<slug:slug>/', views.TrackDetailView.as_view(), name='track_detail'),
    path('discipleship/<slug:track_slug>/request-mentor/', views.request_mentor, name='request_mentor'),
    path('discipleship/<slug:track_slug>/module/<int:module_id>/lesson/<int:lesson_id>/',
         views.lesson_detail, name='lesson_detail'),
    path('mentorship/dashboard/', views.mentorship_dashboard, name='mentorship_dashboard'),
    path('mentorship/<int:relationship_id>/schedule/', views.schedule_meeting, name='schedule_meeting'),

    path('prison/', views.FacilityListView.as_view(), name='facility_list'),
    path('prison/facility/<int:pk>/', views.FacilityDetailView.as_view(), name='facility_detail'),
    path('prison/facility/<int:facility_id>/apply/', views.volunteer_application, name='volunteer_application'),
    path('prison/dashboard/', views.prison_ministry_dashboard, name='prison_ministry_dashboard'),
    path('prison/visit/<int:visit_id>/report/', views.submit_visit_report, name='submit_visit_report'),

    # Hospital List and Details
    path('hospital/', views.HospitalListView.as_view(), name='hospital_list'),
    path('<int:pk>/', views.HospitalDetailView.as_view(), name='hospital_detail'),

    # Volunteer Management
    path('volunteer/register/', views.volunteer_registration, name='volunteer_registration'),
    path('dashboard/', views.hospital_ministry_dashboard, name='dashboard'),

    # Visit Management
    path('visit/<int:visit_id>/report/', views.submit_visit_report, name='submit_report'),
    path('visit/create/', views.VisitCreateView.as_view(), name='visit_create'),
    path('visit/<int:pk>/edit/', views.VisitUpdateView.as_view(), name='visit_edit'),

    # Patient Requests
    path('request/create/', views.patient_request_form, name='patient_request_create'),
    path('request/<int:pk>/', views.PatientRequestDetailView.as_view(), name='request_detail'),








]