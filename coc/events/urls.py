from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('live-streams/', views.live_streams_view, name='live_streams'),
    path('live-streams/<int:stream_id>/', views.stream_detail_view, name='stream_detail'),
    path('live-streams/<int:stream_id>/start/', views.start_stream, name='start_stream'),
    path('live-streams/<int:stream_id>/end/', views.end_stream, name='end_stream'),
    path('missions/', views.missions_view, name='missions_view'),
    path('live_stream/', views.live_streams_view, name='live_stream_view'),
    path('start_stream/<int:stream_id>/', views.start_stream, name='start_stream'),
    path('stream_details/<int:stream_id>/', views.stream_detail_view, name='stream_detail_view'),
    path('end_stream/<int:stream_id>/', views.end_stream, name='end_stream'),

    path('create/', views.create_event, name='create_event'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/register/', views.event_detail, name='event_register'),
    path('<int:pk>/cancel/', views.cancel_registration, name='cancel_registration'),

]
