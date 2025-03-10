import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeProcessor:
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        """Create a payment intent for a one-time payment"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                metadata=metadata or {},
            )
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'id': intent.id
            }
        except Exception as e:
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
                'id': customer.id
            }
        except Exception as e:
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
                'id': subscription.id
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def create_price(amount, currency='usd', recurring=None, product_name='Church Donation'):
        """Create a price for a product"""
        try:
            # Create a product
            product = stripe.Product.create(name=product_name)

            price_data = {
                'unit_amount': int(amount * 100),  # Convert to cents
                'currency': currency,
                'product': product.id,
            }

            if recurring:
                price_data['recurring'] = {
                    'interval': recurring.get('interval', 'month'),
                    'interval_count': recurring.get('interval_count', 1),
                }

            price = stripe.Price.create(**price_data)
            return {
                'success': True,
                'id': price.id
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
