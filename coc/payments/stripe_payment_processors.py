import stripe
from django.conf import settings
from django.urls import reverse
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentProcessor:
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        """Create a payment intent for a one-time payment"""
        amount_cents = int(amount * 100)  # Convert to cents

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
            )
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def create_subscription(customer_id, price_id, metadata=None):
        """Create a subscription for recurring payments"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                metadata=metadata or {},
            )
            return {
                'success': True,
                'subscription_id': subscription.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def create_customer(email, name=None, metadata=None):
        """Create a Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {},
            )
            return {
                'success': True,
                'customer_id': customer.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def create_payment_method(card_number, exp_month, exp_year, cvc):
        """Create a payment method with card details"""
        try:
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'number': card_number,
                    'exp_month': exp_month,
                    'exp_year': exp_year,
                    'cvc': cvc,
                },
            )
            return {
                'success': True,
                'payment_method_id': payment_method.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def attach_payment_method_to_customer(payment_method_id, customer_id):
        """Attach a payment method to a customer"""
        try:
            payment_method = stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id,
            )
            return {
                'success': True,
                'payment_method': payment_method
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def create_price(amount, currency='usd', recurring=None, product_id=None):
        """Create a price for a product"""
        amount_cents = int(amount * 100)  # Convert to cents

        # Create a product if not provided
        if not product_id:
            product = stripe.Product.create(
                name='Church Donation',
                type='service',
            )
            product_id = product.id

        price_data = {
            'unit_amount': amount_cents,
            'currency': currency,
            'product': product_id,
        }

        if recurring:
            price_data['recurring'] = {
                'interval': recurring.get('interval', 'month'),
                'interval_count': recurring.get('interval_count', 1),
            }

        try:
            price = stripe.Price.create(**price_data)
            return {
                'success': True,
                'price_id': price.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
