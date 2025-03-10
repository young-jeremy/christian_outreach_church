from django.conf import settings
from django.db import models


class PaymentMethod(models.Model):
    """Model for saved payment methods"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )

    PAYMENT_TYPE_CHOICES = [
        ('creditCard', 'Credit/Debit Card'),
        ('bankAccount', 'Bank Account'),
    ]

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        default='creditCard'
    )
    card_type = models.CharField(max_length=50, blank=True, null=True)
    last_four = models.CharField(max_length=4)
    expiry_date = models.CharField(max_length=7, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Stripe-specific fields
    stripe_payment_method_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.payment_type == 'creditCard':
            return f"{self.card_type} ending in {self.last_four}"
        else:
            return f"Bank Account ending in {self.last_four}"



class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id}"

    def get_transaction_details(transaction_id):
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            return transaction
        except Transaction.DoesNotExist:
            return None  # Or handle the case where the transaction doesn't exist
