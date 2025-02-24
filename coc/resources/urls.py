from django.urls import path

from . import views
from .views import (
    DailyDevotionListView, DailyDevotionDetailView,
    DailyDevotionCreateView, DailyDevotionUpdateView,
    DailyDevotionDeleteView, BibleStudyMaterialListView,
    BibleStudyMaterialDetailView,

    BibleStudyMaterialDeleteView
)

app_name='resources'

urlpatterns = [
    path('bible-study/', BibleStudyMaterialListView.as_view(), name='bible-study-list'),
    path('bible-study/<int:pk>/', BibleStudyMaterialDetailView.as_view(), name='bible-study-detail'),
    path('bible-study/<int:pk>/delete/', BibleStudyMaterialDeleteView.as_view(), name='bible-study-delete'),

    # ... existing urls ...
    path('devotions/', DailyDevotionListView.as_view(), name='devotion-list'),
    path('devotions/<int:pk>/', DailyDevotionDetailView.as_view(), name='devotion-detail'),
    path('devotions/create/', DailyDevotionCreateView.as_view(), name='devotion-create'),
    path('devotions/<int:pk>/update/', DailyDevotionUpdateView.as_view(), name='devotion-update'),
    path('devotions/<int:pk>/delete/', DailyDevotionDeleteView.as_view(), name='devotion-delete'),

    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/review/', views.BookReviewCreateView.as_view(), name='book_review'),
    path('reading-list/add/', views.AddToReadingListView.as_view(), name='add_to_reading_list'),









]