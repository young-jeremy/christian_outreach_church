from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User


# Audio Messages
class AudioMessage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    speaker = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio_messages/%Y/%m/')
    description = models.TextField()
    recorded_date = models.DateField()
    duration = models.DurationField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('sermon', 'Sermon'),
        ('teaching', 'Teaching'),
        ('testimony', 'Testimony'),
        ('worship', 'Worship'),
    ])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Church News
class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/images/%Y/%m/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Newsletters
class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    issue_number = models.PositiveIntegerField(unique=True)
    publication_date = models.DateField()
    pdf_file = models.FileField(upload_to='newsletters/%Y/%m/')
    cover_image = models.ImageField(upload_to='newsletters/covers/%Y/%m/', blank=True)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return f"Newsletter #{self.issue_number} - {self.title}"


# Announcements
class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='announcements/%Y/%m/', blank=True)
    link = models.URLField(blank=True)

    class Meta:
        ordering = ['-priority', '-start_date']

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return date.today() > self.end_date


# Testimonial Videos
class TestimonialVideo(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    person_name = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='testimonials/%Y/%m/')
    thumbnail = models.ImageField(upload_to='testimonials/thumbnails/%Y/%m/', blank=True)
    description = models.TextField()
    recorded_date = models.DateField()
    approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person_name} - {self.title}"


class PhotoAlbum(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='albums/covers/%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    event_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def photo_count(self):
        return self.photos.count()


class Photo(models.Model):
    album = models.ForeignKey(PhotoAlbum, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='albums/photos/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_photos', blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Photo in {self.album.title}"

    @property
    def like_count(self):
        return self.likes.count()


class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Video Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ArchivedVideo(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='archives/videos/%Y/%m/')
    thumbnail = models.ImageField(upload_to='archives/thumbnails/%Y/%m/', blank=True)
    duration = models.DurationField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-upload_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LiveStream(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    stream_key = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='livestreams/thumbnails/', blank=True, default='coc.png')
    scheduled_time = models.DateTimeField()
    is_live = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    viewers_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-scheduled_time']

    def __str__(self):
        return self.title


class StreamChat(models.Model):
    stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='chats')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']


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