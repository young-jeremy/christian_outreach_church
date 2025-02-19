from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('opportunity/create/', views.opportunity_create, name='opportunity_create'),
    path('opportunity/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunity/<int:pk>/edit/', views.opportunity_edit, name='opportunity_edit'),
    path('opportunity/<int:pk>/signup/', views.volunteer_signup, name='volunteer_signup'),
    path('opportunity/<int:pk>/withdraw/', views.volunteer_withdraw, name='volunteer_withdraw'),
] 