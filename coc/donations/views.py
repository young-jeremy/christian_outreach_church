# donations/views.py
from datetime import datetime

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import UserProfile
from outreach.forms import DonationForm
from .forms import DonationSettingsForm
from .models import Donation
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Donation, DonationSettings
from payments.models import PaymentMethod
from .forms import DonationSettingsForm, DonationForm

# Set up logging
logger = logging.getLogger(__name__)
from payments.stripe_payment_processors import StripePaymentProcessor
from django.conf import settings

from .stripe_processor import StripeProcessor


@login_required
def make_donation_with_stripe(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user

            # Get amount and metadata
            amount = form.cleaned_data['amount']
            metadata = {
                'user_id': str(request.user.id),
                'donation_type': donation.donation_type
            }

            # Process payment based on whether it's recurring
            if form.cleaned_data['recurring']:
                # Get or create Stripe customer
                customer_result = StripeProcessor.create_customer(
                    email=request.user.email,
                    name=request.user.get_full_name(),
                    metadata={'user_id': str(request.user.id)}
                )

                if not customer_result['success']:
                    messages.error(request, f"Error creating customer: {customer_result['error']}")
                    return render(request, 'donations/make_donation.html', {'form': form})

                # Map Django recurring frequency to Stripe interval
                frequency = form.cleaned_data.get('recurring_frequency', 'monthly')
                interval_mapping = {
                    'weekly': {'interval': 'week', 'interval_count': 1},
                    'biweekly': {'interval': 'week', 'interval_count': 2},
                    'monthly': {'interval': 'month', 'interval_count': 1},
                    'quarterly': {'interval': 'month', 'interval_count': 3}
                }

                # Create a price for the recurring donation
                price_result = StripeProcessor.create_price(
                    amount=amount,
                    recurring=interval_mapping.get(frequency, {'interval': 'month', 'interval_count': 1}),
                    product_name=f"Church {donation.get_donation_type_display()}"
                )

                if not price_result['success']:
                    messages.error(request, f"Error creating price: {price_result['error']}")
                    return render(request, 'donations/make_donation.html', {'form': form})

                # Create a subscription
                subscription_result = StripeProcessor.create_subscription(
                    customer_id=customer_result['id'],
                    price_id=price_result['id'],
                    metadata=metadata
                )

                if not subscription_result['success']:
                    messages.error(request, f"Error creating subscription: {subscription_result['error']}")
                    return render(request, 'donations/make_donation.html', {'form': form})

                # Save the subscription ID
                donation.transaction_id = subscription_result['id']
                donation.status = 'completed'

            else:
                # Create a one-time payment intent
                intent_result = StripeProcessor.create_payment_intent(
                    amount=amount,
                    metadata=metadata
                )

                if not intent_result['success']:
                    messages.error(request, f"Error creating payment: {intent_result['error']}")
                    return render(request, 'donations/make_donation.html', {'form': form})

                # Save the payment intent ID
                donation.transaction_id = intent_result['id']
                donation.status = 'completed'

            # Save the donation
            donation.save()

            messages.success(request, f'Thank you for your donation of ${amount}!')
            return redirect('donations:receipt', donation_id=donation.id)
    else:
        form = DonationForm()

    return render(request, 'donations/make_donation.html', {
        'form': form,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })


@login_required
def payment_view(request):
    """Handle payment methods with improved error handling"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                payment_type = request.POST.get('payment_type')

                if payment_type == 'creditCard':
                    # Process credit card form
                    card_number = request.POST.get('card_number', '').strip()
                    expiry_date = request.POST.get('expiry_date', '').strip()
                    cvv = request.POST.get('cvv', '').strip()
                    name_on_card = request.POST.get('name_on_card', '').strip()

                    # Validate inputs
                    if not card_number or not expiry_date or not cvv or not name_on_card:
                        raise ValidationError("All credit card fields are required")

                    # Basic validation (you would use a library for more robust validation)
                    if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
                        raise ValidationError("Invalid card number format")

                    if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
                        raise ValidationError("Invalid CVV format")

                    # In a real implementation, you would use a payment processor API here
                    # For demonstration, we'll just save a masked version
                    last_four = card_number[-4:] if len(card_number) >= 4 else '0000'
                    masked_number = '*' * (len(card_number) - 4) + last_four

                    # Determine card type based on first digits (simplified)
                    card_type = 'Unknown'
                    if card_number.startswith('4'):
                        card_type = 'Visa'
                    elif card_number.startswith('5'):
                        card_type = 'MasterCard'
                    elif card_number.startswith('3'):
                        card_type = 'American Express'
                    elif card_number.startswith('6'):
                        card_type = 'Discover'

                    # Save payment method to database
                    payment_method = PaymentMethod(
                        user=request.user,
                        payment_type='creditCard',
                        card_type=card_type,
                        last_four=last_four,
                        expiry_date=expiry_date
                    )

                    # Set as default if requested or if it's the first payment method
                    set_as_default = request.POST.get('set_as_default') == 'on'
                    if set_as_default or not PaymentMethod.objects.filter(user=request.user).exists():
                        payment_method.is_default = True
                        # Clear default status from other payment methods
                        PaymentMethod.objects.filter(user=request.user).update(is_default=False)

                    payment_method.save()

                    messages.success(request,
                                     f'Your {card_type} card ending in {last_four} has been added successfully.')

                elif payment_type == 'bankAccount':
                    # Process bank account form
                    account_name = request.POST.get('account_name', '').strip()
                    routing_number = request.POST.get('routing_number', '').strip()
                    account_number = request.POST.get('account_number', '').strip()
                    account_type = request.POST.get('account_type', '').strip()

                    # Validate inputs
                    if not account_name or not routing_number or not account_number or not account_type:
                        raise ValidationError("All bank account fields are required")

                    # Basic validation
                    if not routing_number.isdigit() or len(routing_number) != 9:
                        raise ValidationError("Invalid routing number format. Must be 9 digits.")

                    if not account_number.isdigit() or len(account_number) < 5:
                        raise ValidationError("Invalid account number format")

                    # In a real implementation, you would verify the routing number
                    # and possibly use a service like Plaid for account verification

                    # Save payment method to database
                    last_four = account_number[-4:] if len(account_number) >= 4 else '0000'

                    payment_method = PaymentMethod(
                        user=request.user,
                        payment_type='bankAccount',
                        card_type=f'{account_type.capitalize()} Account',
                        last_four=last_four
                    )

                    # Set as default if requested or if it's the first payment method
                    set_as_default = request.POST.get('set_as_default') == 'on'
                    if set_as_default or not PaymentMethod.objects.filter(user=request.user).exists():
                        payment_method.is_default = True
                        # Clear default status from other payment methods
                        PaymentMethod.objects.filter(user=request.user).update(is_default=False)

                    payment_method.save()

                    messages.success(request,
                                     f'Your {account_type} account ending in {last_four} has been added successfully.')

                else:
                    raise ValidationError("Invalid payment type selected")

                return redirect('donations:payment_view')

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            logger.error(f"Error processing payment method: {str(e)}", exc_info=True)
            messages.error(request, "An unexpected error occurred. Please try again later.")

    # Get user's saved payment methods
    payment_methods = PaymentMethod.objects.filter(user=request.user).order_by('-is_default', '-created_at')

    return render(request, 'donations/payment_view.html', {
        'payment_methods': payment_methods
    })


@login_required
def make_donation(request):
    """Handle making a donation with improved error handling"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = DonationForm(request.POST)
                if not form.is_valid():
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")
                    raise ValidationError("Please correct the errors in the form.")

                donation = form.save(commit=False)
                donation.user = request.user

                # Validate amount
                amount = form.cleaned_data.get('amount')
                if amount <= 0:
                    raise ValidationError("Donation amount must be greater than zero.")

                # Get payment method details
                payment_method_id = request.POST.get('payment_method')

                if payment_method_id == 'new':
                    # Process new payment method
                    payment_type = request.POST.get('payment_type')

                    if payment_type == 'creditCard':
                        # Validate credit card details
                        card_number = request.POST.get('card_number', '').strip()
                        expiry_date = request.POST.get('expiry_date', '').strip()
                        cvv = request.POST.get('cvv', '').strip()
                        name_on_card = request.POST.get('name_on_card', '').strip()

                        if not card_number or not expiry_date or not cvv or not name_on_card:
                            raise ValidationError("All credit card fields are required")

                        # In a real implementation, you would process the payment through a payment gateway
                        # For demonstration, we'll just record the payment method
                        last_four = card_number[-4:] if len(card_number) >= 4 else '0000'
                        donation.payment_method = "Credit Card"
                        donation.payment_last_four = last_four

                        # Save the payment method if requested
                        if request.POST.get('save_payment_method') == 'on':
                            card_type = 'Credit Card'
                            if card_number.startswith('4'):
                                card_type = 'Visa'
                            elif card_number.startswith('5'):
                                card_type = 'MasterCard'
                            elif card_number.startswith('3'):
                                card_type = 'American Express'
                            elif card_number.startswith('6'):
                                card_type = 'Discover'

                            payment_method = PaymentMethod(
                                user=request.user,
                                payment_type='creditCard',
                                card_type=card_type,
                                last_four=last_four,
                                expiry_date=expiry_date
                            )
                            payment_method.save()

                    elif payment_type == 'bankAccount':
                        # Validate bank account details
                        account_name = request.POST.get('account_name', '').strip()
                        routing_number = request.POST.get('routing_number', '').strip()
                        account_number = request.POST.get('account_number', '').strip()
                        account_type = request.POST.get('account_type', '').strip()

                        if not account_name or not routing_number or not account_number or not account_type:
                            raise ValidationError("All bank account fields are required")

                        # In a real implementation, you would process the ACH payment
                        # For demonstration, we'll just record the payment method
                        last_four = account_number[-4:] if len(account_number) >= 4 else '0000'
                        donation.payment_method = f"{account_type.capitalize()} Account"
                        donation.payment_last_four = last_four

                        # Save the payment method if requested
                        if request.POST.get('save_payment_method') == 'on':
                            payment_method = PaymentMethod(
                                user=request.user,
                                payment_type='bankAccount',
                                card_type=f'{account_type.capitalize()} Account',
                                last_four=last_four
                            )
                            payment_method.save()

                    else:
                        raise ValidationError("Invalid payment type selected")

                elif payment_method_id and payment_method_id != 'new':
                    try:
                        payment_method = PaymentMethod.objects.get(id=payment_method_id, user=request.user)
                        donation.payment_method = payment_method.get_payment_type_display()
                        donation.payment_last_four = payment_method.last_four

                        # In a real implementation, you would use the saved payment method
                        # to process the payment through a payment gateway
                    except PaymentMethod.DoesNotExist:
                        raise ValidationError("Selected payment method not found")
                else:
                    raise ValidationError("Please select a payment method")

                # Process recurring donation if selected
                if form.cleaned_data.get('recurring'):
                    recurring_frequency = request.POST.get('recurring_frequency', 'monthly')
                    donation.recurring_frequency = recurring_frequency

                    # In a real implementation, you would set up a recurring payment
                    # with your payment processor

                # Process the payment (this would be handled by your payment gateway in production)
                # For demonstration, we'll simulate a successful payment
                donation.status = 'completed'
                donation.save()

                # If this is a recurring donation, update user's donation settings
                if form.cleaned_data.get('recurring'):
                    donation_settings, created = DonationSettings.objects.get_or_create(user=request.user)

                    if donation.donation_type == 'tithe':
                        donation_settings.recurring_tithe = True
                    elif donation.donation_type == 'missions':
                        donation_settings.recurring_missions = True
                    elif donation.donation_type == 'building':
                        donation_settings.recurring_building_fund = True

                    donation_settings.save()

                messages.success(request, f'Thank you for your generous donation of ${amount}!')
                return redirect('donations:receipt', donation_id=donation.id)

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            logger.error(f"Error processing donation: {str(e)}", exc_info=True)
            messages.error(request,
                           "An unexpected error occurred while processing your donation. Please try again later.")
    else:
        form = DonationForm()

    # Get user's saved payment methods
    saved_payment_methods = PaymentMethod.objects.filter(user=request.user).order_by('-is_default', '-created_at')

    return render(request, 'donations/make_donation.html', {
        'form': form,
        'saved_payment_methods': saved_payment_methods
    })


@login_required
def set_default_payment(request, payment_id):
    """Set a payment method as default with error handling"""
    try:
        payment_method = get_object_or_404(PaymentMethod, id=payment_id, user=request.user)

        # Clear default status from all other payment methods
        PaymentMethod.objects.filter(user=request.user).update(is_default=False)

        # Set this payment method as default
        payment_method.is_default = True
        payment_method.save()

        messages.success(request, 'Default payment method updated successfully.')
    except Exception as e:
        logger.error(f"Error setting default payment method: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while updating your default payment method.")

    return redirect('donations:payment_view')


@login_required
def delete_payment(request, payment_id):
    """Delete a payment method with error handling"""
    try:
        payment_method = get_object_or_404(PaymentMethod, id=payment_id, user=request.user)

        # Check if this is the default payment method
        is_default = payment_method.is_default

        # Delete the payment method
        payment_method.delete()

        # If this was the default payment method, set another one as default
        if is_default:
            try:
                new_default = PaymentMethod.objects.filter(user=request.user).first()
                if new_default:
                    new_default.is_default = True
                    new_default.save()
            except PaymentMethod.DoesNotExist:
                pass

        messages.success(request, 'Payment method deleted successfully.')
    except Exception as e:
        logger.error(f"Error deleting payment method: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while deleting your payment method.")

    return redirect('donations:payment_view')


@login_required
def donation_settings(request):
    """Handle donation settings updates"""
    if request.method == 'POST':
        form = DonationSettingsForm(request.POST, instance=request.user.donation_settings)
        if form.is_valid():
            form.save()

            # Handle recurring donation amounts
            if form.cleaned_data.get('recurring_tithe'):
                tithe_amount = request.POST.get('tithe_amount', 0)
                # Save tithe amount to user's settings

            if form.cleaned_data.get('recurring_missions'):
                missions_amount = request.POST.get('missions_amount', 0)
                # Save missions amount to user's settings

            if form.cleaned_data.get('recurring_building_fund'):
                building_amount = request.POST.get('building_amount', 0)
                # Save building fund amount to user's settings

            messages.success(request, 'Your donation settings have been updated successfully.')
            return redirect('accounts:accounts_settings_and_privacy')
    else:
        form = DonationSettingsForm(instance=request.user.donation_settings)

    # Get current recurring amounts
    tithe_amount = 0  # Get from user settings
    missions_amount = 0  # Get from user settings
    building_amount = 0  # Get from user settings

    return render(request, 'donations/settings_form.html', {
        'form': form,
        'tithe_amount': tithe_amount,
        'missions_amount': missions_amount,
        'building_amount': building_amount
    })


@login_required
def donation_receipt(request, donation_id):
    """Display donation receipt"""
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)

    return render(request, 'donations/donation_receipt.html', {
        'donation': donation
    })


@login_required
def donation_history(request):
    """Display donation history"""
    donations = request.user.donations.all()
    return render(request, 'donations/history.html', {'donations': donations})


@login_required
def tax_statement(request):
    """Display tax statement"""
    year = request.GET.get('year', datetime.now().year - 1)  # Default to previous year

    # Get user's donations for the specified year
    donations = request.user.donations.filter(date__year=year).order_by('date')

    # Calculate totals
    total_donations = sum(donation.amount for donation in donations)

    # Calculate fund totals
    tithe_total = sum(donation.amount for donation in donations if donation.donation_type == 'tithe')
    missions_total = sum(donation.amount for donation in donations if donation.donation_type == 'missions')
    building_total = sum(donation.amount for donation in donations if donation.donation_type == 'building')
    other_total = sum(donation.amount for donation in donations if donation.donation_type == 'other')

    # Generate statement ID
    statement_id = f"ST-{year}-{request.user.id:03d}"

    return render(request, 'donations/tax_statement.html', {
        'donations': donations,
        'total_donations': total_donations,
        'tithe_total': tithe_total,
        'missions_total': missions_total,
        'building_total': building_total,
        'other_total': other_total,
        'year': year,
        'statement_id': statement_id,
        'statement_date': datetime.now()
    })
