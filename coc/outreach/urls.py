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




]