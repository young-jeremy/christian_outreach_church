# views.py
from django.conf import settings
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from donations.models import DonationSettings, Donation
from .models import *

mpesa_client = MpesaClient()
from .paypal_payment_processors import PayPalPaymentProcessor
from django.urls import reverse
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
from twilio.rest import Client


def process_text_donation(phone_number, amount, donation_type):
    # Set up Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send confirmation message
    message = client.messages.create(
        body=f"Thank you for your {donation_type} donation of ${amount}. Reply YES to confirm.",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    # In a real implementation, you would set up a webhook to handle the reply
    # and process the payment when the user confirms

    return message.sid


@login_required
def paypal_create_payment(request):
    """Create a PayPal payment and redirect to PayPal"""
    try:
        # Get donation details from session
        donation_data = request.session.get('donation_data', {})
        if not donation_data:
            messages.error(request, "Donation information not found. Please try again.")
            return redirect('donations:make_donation')

        amount = donation_data.get('amount')

        # Create return and cancel URLs
        return_url = request.build_absolute_uri(reverse('donations:paypal_execute_payment'))
        cancel_url = request.build_absolute_uri(reverse('donations:make_donation'))

        # Create PayPal payment
        result = PayPalPaymentProcessor.create_payment(
            amount=amount,
            return_url=return_url,
            cancel_url=cancel_url,
            description=f"Church Donation - {donation_data.get('donation_type', 'General')}"
        )

        if result['success']:
            # Store the payment ID in session
            request.session['paypal_payment_id'] = result['payment_id']

            # Redirect to PayPal approval URL
            return redirect(result['approval_url'])
        else:
            messages.error(request, f"Failed to create PayPal payment: {result.get('error')}")
            return redirect('donations:make_donation')

    except Exception as e:
        logger.error(f"Error creating PayPal payment: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect('donations:make_donation')


@login_required
def paypal_execute_payment(request):
    """Execute a PayPal payment after user approval"""
    try:
        payment_id = request.session.get('paypal_payment_id')
        payer_id = request.GET.get('PayerID')

        if not payment_id or not payer_id:
            messages.error(request, "Payment information not found. Please try again.")
            return redirect('donations:make_donation')

        # Execute the payment
        result = PayPalPaymentProcessor.execute_payment(
            payment_id=payment_id,
            payer_id=payer_id
        )

        if result['success']:
            # Get donation details from session
            donation_data = request.session.get('donation_data', {})

            # Create the donation record
            donation = Donation(
                user=request.user,
                amount=donation_data.get('amount'),
                donation_type=donation_data.get('donation_type', 'tithe'),
                recurring=donation_data.get('recurring', False),
                payment_method='PayPal',
                status='completed',
                transaction_id=payment_id
            )

            if donation_data.get('recurring'):
                donation.recurring_frequency = donation_data.get('recurring_frequency', 'monthly')

            donation.save()

            # Clear session data
            if 'donation_data' in request.session:
                del request.session['donation_data']
            if 'paypal_payment_id' in request.session:
                del request.session['paypal_payment_id']

            messages.success(request, f"Thank you for your generous donation of ${donation.amount}!")
            return redirect('donations:receipt', donation_id=donation.id)
        else:
            messages.error(request, f"Failed to complete PayPal payment: {result.get('error')}")
            return redirect('donations:make_donation')

    except Exception as e:
        logger.error(f"Error executing PayPal payment: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect('donations:make_donation')


@login_required
def paypal_create_subscription(request):
    """Create a PayPal subscription for recurring donations"""
    try:
        # Get donation details from session
        donation_data = request.session.get('donation_data', {})
        if not donation_data:
            messages.error(request, "Donation information not found. Please try again.")
            return redirect('donations:make_donation')

        amount = donation_data.get('amount')
        recurring_frequency = donation_data.get('recurring_frequency', 'monthly')

        # Map Django recurring frequency to PayPal frequency
        frequency_mapping = {
            'weekly': 'WEEK',
            'biweekly': 'WEEK',  # PayPal doesn't have biweekly, we'll handle this differently
            'monthly': 'MONTH',
            'quarterly': 'MONTH'  # PayPal doesn't have quarterly, we'll handle this differently
        }

        paypal_frequency = frequency_mapping.get(recurring_frequency, 'MONTH')

        # Create a billing plan
        plan_result = PayPalPaymentProcessor.create_billing_plan(
            amount=amount,
            frequency=paypal_frequency,
            description=f"Church Recurring Donation - {donation_data.get('donation_type', 'General')}"
        )

        if not plan_result['success']:
            messages.error(request, f"Failed to create subscription plan: {plan_result.get('error')}")
            return redirect('donations:make_donation')

        # Calculate start date (24 hours from now to allow for PayPal processing)
        start_date = (datetime.now() + timedelta(hours=24)).isoformat()

        # Create a billing agreement
        agreement_result = PayPalPaymentProcessor.create_billing_agreement(
            plan_id=plan_result['plan_id'],
            start_date=start_date,
            description=f"Church Recurring Donation - {donation_data.get('donation_type', 'General')}"
        )

        if agreement_result['success']:
            # Store the agreement ID in session
            request.session['paypal_agreement_id'] = agreement_result['agreement_id']

            # Redirect to PayPal approval URL
            return redirect(agreement_result['approval_url'])
        else:
            messages.error(request, f"Failed to create subscription: {agreement_result.get('error')}")
            return redirect('donations:make_donation')

    except Exception as e:
        logger.error(f"Error creating PayPal subscription: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect('donations:make_donation')


@login_required
def paypal_execute_agreement(request):
    """Execute a PayPal billing agreement after user approval"""
    try:
        token = request.GET.get('token')

        if not token:
            messages.error(request, "Agreement information not found. Please try again.")
            return redirect('donations:make_donation')

        # Execute the agreement
        result = PayPalPaymentProcessor.execute_agreement(token=token)

        if result['success']:
            # Get donation details from session
            donation_data = request.session.get('donation_data', {})

            # Create the donation record
            donation = Donation(
                user=request.user,
                amount=donation_data.get('amount'),
                donation_type=donation_data.get('donation_type', 'tithe'),
                recurring=True,
                recurring_frequency=donation_data.get('recurring_frequency', 'monthly'),
                payment_method='PayPal',
                status='completed',
                transaction_id=result['agreement_id']
            )
            donation.save()

            # Update user's donation settings for recurring donations
            donation_settings, created = DonationSettings.objects.get_or_create(user=request.user)

            if donation.donation_type == 'tithe':
                donation_settings.recurring_tithe = True
            elif donation.donation_type == 'missions':
                donation_settings.recurring_missions = True
            elif donation.donation_type == 'building':
                donation_settings.recurring_building_fund = True

            donation_settings.save()

            # Clear session data
            if 'donation_data' in request.session:
                del request.session['donation_data']
            if 'paypal_agreement_id' in request.session:
                del request.session['paypal_agreement_id']

            messages.success(request, f"Thank you for setting up a recurring donation of ${donation.amount}!")
            return redirect('donations:receipt', donation_id=donation.id)
        else:
            messages.error(request, f"Failed to complete subscription: {result.get('error')}")
            return redirect('donations:make_donation')

    except Exception as e:
        logger.error(f"Error executing PayPal agreement: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect('donations:make_donation')




def payment_view(request):
    template_name = 'payments/payment_view.html'
    phone_number = '+254728429010'  # Replace with customer phone number
    amount = 3000  # Amount to be paid
    account_reference = 'Crout'
    transaction_desc = 'Payment for Service'

    callback_url = settings.CALLBACK_URL
    response = mpesa_client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

    if hasattr(response, 'json'):
        response_dict = response.json()
    else:
        # If it's a custom response type, extract necessary fields
        response_dict = {
            'status': 'Payment initiated',
            'message': str(response),  # Convert response object to string if needed
        }

    return render(request, template_name)

@csrf_exempt
def payment_callback(request):
    # Process the callback data from M-Pesa here
    data = request.body.decode('utf-8')
    # Perform your logic, e.g., update the payment status in your database
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


def request_service_view(request):
    if request.method == 'POST':
        service = request.POST.get('service')
        phone_number = request.POST.get('phone_number')
        amount = 1000  # Set a predefined amount or vary based on service
        account_reference = 'ServiceUpgrade'
        transaction_desc = f'Request for {service} service'
        callback_url = request.build_absolute_uri('/payments/callback/')

        # Initiate M-Pesa STK Push
        response = mpesa_client.stk_push(
            phone_number,
            amount,
            account_reference,
            transaction_desc,
            callback_url
        )

        if response['ResponseCode'] == '0':
            return JsonResponse({"status": "Payment initiated. Check your phone to complete payment."})
        else:
            return JsonResponse({"status": "Failed to initiate payment. Try again later."})

    return render(request, 'dashboard/pages-invoice.html')


@csrf_exempt
def payment_callback(request):
    data = request.body.decode('utf-8')
    # Log or process callback data (e.g., update payment status in your database)
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


def invoice_view(request, transaction_id):
    # Fetch transaction details from the database (or session)
    try:
        transaction = get_transaction_details(transaction_id)  # Define this function
    except Transaction.DoesNotExist:
        raise Http404("Transaction not found")

    # Render the invoice page with the transaction details
    return render(request, 'payments/invoice.html', {'transaction': transaction})
