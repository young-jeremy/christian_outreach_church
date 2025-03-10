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

    path('stream_list/', views.stream_list, name='stream_list_view'),
    path('stream_list/<int:stream_id>/', views.stream_list, name='stream_list_view'),
    path('stream_details/<int:stream_id>/', views.stream_detail, name='stream_detail_view'),
    path('stream_details/<int:stream_id>/', views.stream_detail, name='stream_detail_view'),
    path('stream_details/<int:stream_id>/start/', views.start_stream, name='start_stream'),
    path('stream_details/<int:stream_id>/end/', views.end_stream, name='end_stream'),
    path('stream_details/<int:stream_id>/register/', views.event_detail, name='event_detail'),
    path('create_stream/', views.create_stream, name='create_stream'),
    path('streams/', views.stream_list, name='stream_list'),
    path('streams/create/', views.create_stream, name='create_stream'),
    path('streams/<int:stream_id>/', views.stream_detail, name='stream_detail'),
    path('streams/<int:stream_id>/chat/', views.post_chat, name='post_chat'),

    path('videos/', views.video_list, name='video_list'),
    path('videos/upload/', views.upload_video, name='upload_video'),
    path('videos/search/', views.search_videos, name='search_videos'),
    path('videos/category/<slug:slug>/', views.category_videos, name='category_videos'),
    path('videos/<slug:slug>/', views.video_detail, name='video_detail'),

    # ... other URLs ...
    path('gallery/', views.album_list, name='album_list'),
    path('gallery/create/', views.create_album, name='create_album'),
    path('gallery/<slug:slug>/', views.album_detail, name='album_detail'),
    path('gallery/<slug:album_slug>/upload/', views.upload_photos, name='upload_photos'),
    path('gallery/photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),

    # Audio Messages

    path('audio/', views.audio_message_list, name='audio_message_list'),
    path('audio/create/', views.audio_message_create, name='audio_message_create'),
    path('audio/<slug:slug>/', views.audio_message_detail, name='audio_message_detail'),
    path('audio-messages/<slug:slug>/edit/', views.audio_message_edit, name='audio_message_edit'),
    path('audio-messages/<slug:slug>/delete/', views.audio_message_delete, name='audio_message_delete'),

    # News Articles
    path('news/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    # Newsletters
    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/create/', views.newsletter_create, name='newsletter_create'),
    path('newsletters/<int:issue_number>/', views.newsletter_detail, name='newsletter_detail'),

    # Announcements
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),

    # Testimonials
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('testimonials/create/', views.testimonial_create, name='testimonial_create'),
    path('testimonials/<slug:slug>/', views.testimonial_detail, name='testimonial_detail'),
    path('testimonials/<slug:slug>/edit/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/<slug:slug>/delete/', views.testimonial_delete, name='testimonial_delete'),

]
