# donations/models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings


class DonationSettings(models.Model):
    """Model for user donation settings"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donation_settings'
    )

    PAYMENT_METHOD_CHOICES = [
        ('creditCard', 'Credit/Debit Card'),
        ('bankTransfer', 'Bank Transfer (ACH)'),
        ('paypal', 'PayPal'),
    ]

    RECEIPT_CHOICES = [
        ('immediately', 'Send immediately'),
        ('monthly', 'Send monthly summary'),
        ('quarterly', 'Send quarterly summary'),
        ('annually', 'Send annual summary only'),
    ]

    recurring_tithe = models.BooleanField(default=False)
    recurring_missions = models.BooleanField(default=False)
    recurring_building_fund = models.BooleanField(default=False)
    preferred_payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='creditCard'
    )
    donation_receipts = models.CharField(
        max_length=20,
        choices=RECEIPT_CHOICES,
        default='immediately'
    )

    def __str__(self):
        return f"{self.user.username}'s Donation Settings"


class Donation(models.Model):
    """Model for donations"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donations'
    )

    DONATION_TYPE_CHOICES = [
        ('tithe', 'Tithe'),
        ('missions', 'Missions Fund'),
        ('building', 'Building Fund'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    RECURRING_FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(
        max_length=20,
        choices=DONATION_TYPE_CHOICES,
        default='tithe'
    )
    date = models.DateTimeField(auto_now_add=True)
    recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(
        max_length=20,
        choices=RECURRING_FREQUENCY_CHOICES,
        default='monthly',
        blank=True,
        null=True
    )
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_last_four = models.CharField(max_length=4, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.get_donation_type_display()})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_donation_settings(sender, instance, created, **kwargs):
    if created:
        DonationSettings.objects.create(user=instance)
