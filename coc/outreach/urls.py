from django.urls import path
from . import views

app_name = 'outreach'
urlpatterns = [
    path('', views.blogs_home, name='outreach'),
    path('live-streams/', views.live_streams, name='live_streams'),
    path('sermons/', views.sermons, name='sermons'),
    path('', views.dashboard_view, name='dashboard'),
    path('sermons/', views.sermons_view, name='sermons'),
    path('bible-studies/', views.bible_studies_view, name='bible_studies'),
    path('prayer-requests/', views.prayer_requests_view, name='prayer_requests'),
    path('small-groups/', views.small_groups_view, name='small_groups'),
    path('events/', views.events_view, name='events'),
    path('devotionals/', views.devotionals_view, name='devotionals'),
    path('missions/', views.missions_view, name='missions'),

]
