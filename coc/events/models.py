from django.db import models
from accounts.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import datetime


class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    stream_key = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='stream_thumbnails/', null=True, blank=True)
    scheduled_time = models.DateTimeField(default=timezone.now)
    actual_start_time = models.DateTimeField(null=True, default=timezone.now)
    is_live = models.BooleanField(default=False)
    streamer = models.ForeignKey(User, on_delete=models.CASCADE)
    viewers_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-scheduled_time']


class Event(models.Model):
    EVENT_TYPES = [
        ('service', 'Church Service'),
        ('meeting', 'Meeting'),
        ('workshop', 'Workshop'),
        ('social', 'Social Event'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    
    # Date and Time fields
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    
    # Location fields
    is_online = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True)
    online_link = models.URLField(blank=True, null=True)
    
    # Registration fields
    registration_required = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    
    # Other fields
    is_recurring = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    speakers = models.ManyToManyField(
        User,
        through='EventSpeakers',
        related_name='speaking_events',
        blank=True
    )

    class Meta:
        ordering = ['start_date', 'start_time']

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        now = timezone.now()

        if self.end_date and self.end_time:
            event_end = datetime.combine(self.end_date, self.end_time)

            # Ensure timezone-aware datetime if required
            if timezone.is_naive(event_end):
                event_end = timezone.make_aware(event_end)

            return event_end < now
        return False  # Default case if date or time is missing


class EventSpeakers(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200, blank=True, null=True)
    speaking_time = models.TimeField(null=True, blank=True)
    is_main_speaker = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Event Speaker'
        verbose_name_plural = 'Event Speakers'
        unique_together = ('event', 'speaker')

    def __str__(self):
        return f"{self.speaker.get_full_name()} - {self.event.title}"