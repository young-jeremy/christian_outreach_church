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
    # ... other URLs ...
    path('tools/', views.ToolListView.as_view(), name='tool_list'),
    path('tools/<slug:slug>/', views.ToolDetailView.as_view(), name='tool_detail'),
    path('tools/create/', views.ToolCreateView.as_view(), name='tool_create'),
    path('tools/<slug:slug>/edit/', views.ToolUpdateView.as_view(), name='tool_edit'),
    path('tools/<slug:slug>/download/', views.download_tool, name='tool_download'),
]
