from django.urls import path
from .views import BibleStudyMaterialListView, BibleStudyMaterialDetailView, BibleStudyMaterialCreateView, BibleStudyMaterialUpdateView, BibleStudyMaterialDeleteView

app_name='resources'

urlpatterns = [
    path('bible-study/', BibleStudyMaterialListView.as_view(), name='bible-study-list'),
    path('bible-study/<int:pk>/', BibleStudyMaterialDetailView.as_view(), name='bible-study-detail'),
    path('bible-study/create/', BibleStudyMaterialCreateView.as_view(), name='bible-study-create'),
    path('bible-study/<int:pk>/update/', BibleStudyMaterialUpdateView.as_view(), name='bible-study-update'),
    path('bible-study/<int:pk>/delete/', BibleStudyMaterialDeleteView.as_view(), name='bible-study-delete'),
]