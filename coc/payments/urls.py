from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('initiate/', views.payment_view, name='payment_view'),
    path('payments/callback/', views.payment_callback, name='payment_callback'),
    path('request-service/', views.request_service_view, name='request_service'),
    path('payments/callback/', views.payment_callback, name='payment_callback'),

    # PayPal URLs
    path('paypal/create-payment/', views.paypal_create_payment, name='paypal_create_payment'),
    path('paypal/execute-payment/', views.paypal_execute_payment, name='paypal_execute_payment'),
    path('paypal/create-subscription/', views.paypal_create_subscription, name='paypal_create_subscription'),
    path('paypal/execute-agreement/', views.paypal_execute_agreement, name='paypal_execute_agreement'),

]