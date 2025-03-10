# donations/urls.py
from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('settings/', views.donation_settings, name='settings'),
    path('payment_view/', views.payment_view, name='payment_view'),
    path('settings/', views.donation_settings, name='settings'),
    path('payment_view/', views.payment_view, name='payment_view'),
    path('history/', views.donation_history, name='history'),
    path('receipt/<int:donation_id>/', views.donation_receipt, name='receipt'),
    path('make_donation/', views.make_donation, name='make_donation'),
    path('tax_statement/', views.tax_statement, name='tax_statement'),  # This is the missing URL pattern
    path('set_default_payment/<int:payment_id>/', views.set_default_payment, name='set_default_payment'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
]
