from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    duration = models.DurationField()
    slots = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open'),
            ('filled', 'Filled'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed'),
        ],
        default='open'
    )

    class Meta:
        verbose_name_plural = "Opportunities"
        ordering = ['-date']

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.date < timezone.now()

class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    signed_up_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('declined', 'Declined'),
            ('completed', 'Completed'),
        ],
        default='pending'
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'opportunity']
        ordering = ['-signed_up_at']

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}" 