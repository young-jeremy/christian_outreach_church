import paypalrestsdk
from django.conf import settings
from django.urls import reverse
from decimal import Decimal

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # "sandbox" or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


class PayPalPaymentProcessor:
    @staticmethod
    def create_payment(amount, return_url, cancel_url, description="Church Donation"):
        """Create a PayPal payment"""
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": "USD"
                },
                "description": description
            }]
        })

        try:
            if payment.create():
                # Extract the approval URL
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        return {
                            'success': True,
                            'payment_id': payment.id,
                            'approval_url': approval_url
                        }
            else:
                return {
                    'success': False,
                    'error': payment.error
                }
        except paypalrestsdk.exceptions.ConnectionError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def execute_payment(payment_id, payer_id):
        """Execute a PayPal payment after approval"""
        payment = paypalrestsdk.Payment.find(payment_id)

        try:
            if payment.execute({"payer_id": payer_id}):
                return {
                    'success': True,
                    'payment': payment.to_dict()
                }
            else:
                return {
                    'success': False,
                    'error': payment.error
                }
        except paypalrestsdk.exceptions.ConnectionError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def create_billing_plan(amount, frequency, description="Church Recurring Donation"):
        """Create a PayPal billing plan for recurring payments"""
        billing_plan = paypalrestsdk.BillingPlan({
            "name": "Church Recurring Donation Plan",
            "description": description,
            "type": "INFINITE",
            "payment_definitions": [
                {
                    "name": "Regular Donation",
                    "type": "REGULAR",
                    "frequency": frequency.upper(),
                    "frequency_interval": "1",
                    "amount": {
                        "value": str(amount),
                        "currency": "USD"
                    },
                    "cycles": "0"
                }
            ],
            "merchant_preferences": {
                "setup_fee": {
                    "value": "0",
                    "currency": "USD"
                },
                "return_url": "http://example.com/return",
                "cancel_url": "http://example.com/cancel",
                "auto_bill_amount": "YES",
                "initial_fail_amount_action": "CONTINUE",
                "max_fail_attempts": "3"
            }
        })

        try:
            if billing_plan.create():
                # Activate the plan
                billing_plan.replace([
                    {
                        "op": "replace",
                        "path": "/",
                        "value": {
                            "state": "ACTIVE"
                        }
                    }
                ])

                return {
                    'success': True,
                    'plan_id': billing_plan.id
                }
            else:
                return {
                    'success': False,
                    'error': billing_plan.error
                }
        except paypalrestsdk.exceptions.ConnectionError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def create_billing_agreement(plan_id, start_date, description="Church Recurring Donation"):
        """Create a PayPal billing agreement for a plan"""
        billing_agreement = paypalrestsdk.BillingAgreement({
            "name": "Church Recurring Donation Agreement",
            "description": description,
            "start_date": start_date,
            "plan": {
                "id": plan_id
            },
            "payer": {
                "payment_method": "paypal"
            }
        })

        try:
            if billing_agreement.create():
                # Extract the approval URL
                for link in billing_agreement.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        return {
                            'success': True,
                            'agreement_id': billing_agreement.id,
                            'approval_url': approval_url
                        }
            else:
                return {
                    'success': False,
                    'error': billing_agreement.error
                }
        except paypalrestsdk.exceptions.ConnectionError as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def execute_agreement(token):
        """Execute a PayPal billing agreement after approval"""
        try:
            billing_agreement = paypalrestsdk.BillingAgreement.execute(token)
            return {
                'success': True,
                'agreement_id': billing_agreement.id
            }
        except paypalrestsdk.exceptions.ConnectionError as e:
            return {
                'success': False,
                'error': str(e)
            }
