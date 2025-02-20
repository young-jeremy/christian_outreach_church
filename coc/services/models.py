from django.contrib import messages
from django.db import models
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
    RegexValidator
)
from django_summernote.fields import SummernoteTextField
from datetime import datetime, date, timedelta, time

# Optional but recommended for type hints
from typing import List, Optional

# Get the User model
User = settings.AUTH_USER_MODEL

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_summernote.fields import SummernoteTextField
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import importlib

importlib.invalidate_caches()
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import mark_safe
import markdown
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

class WomensMinistry(models.Model):
    MINISTRY_TYPE_CHOICES = [
        ('BIBLE_STUDY', 'Bible Study'),
        ('PRAYER_GROUP', 'Prayer Group'),
        ('MENTORSHIP', 'Mentorship'),
        ('OUTREACH', 'Outreach'),
        ('WORKSHOP', 'Workshop'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='led_womens_ministries')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='womens_ministry_memberships', blank=True)
    ministry_type = models.CharField(max_length=50, choices=MINISTRY_TYPE_CHOICES)
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='womens_ministry/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Women's Ministries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('videos:womens_ministry_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class MinistryEvent(models.Model):
    ministry = models.ForeignKey(WomensMinistry, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='womens_ministry_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ministry_events/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.ministry.title}"



class WorshipService(models.Model):
    SERVICE_TYPES = [
        ('sunday', 'Sunday Service'),
        ('midweek', 'Midweek Service'),
        ('special', 'Special Service'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    date = models.DateTimeField()
    theme = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # Location
    location = models.CharField(max_length=200, null=True)
    is_online = models.BooleanField(default=False)
    live_stream_url = models.URLField(blank=True)
    meeting_link = models.URLField(blank=True)

    # Leaders
    worship_leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='led_services'
    )
    preacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preached_services',
        null=True,
        blank=True
    )
    team_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='service_team_members',
        blank=True
    )

    # Content
    song_list = models.TextField(blank=True)
    service_order = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    special_notes = models.TextField(blank=True)

    # Media
    image = models.ImageField(upload_to='worship_services/images/', blank=True, null=True)
    banner = models.ImageField(upload_to='worship_services/banners/', blank=True, null=True)

    # Registration
    registration_required = models.BooleanField(default=False)
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)

    # Flags
    is_featured = models.BooleanField(default=False)
    is_special_event = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Worship Service"
        verbose_name_plural = "Worship Services"

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"



class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Forum Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def total_posts(self):
        return sum(topic.posts.count() for topic in self.topics.all())

    def latest_topic(self):
        return self.topics.order_by('-created_at').first()


class ForumTopic(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='topics')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply_form = models.TextField(null=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    def replies_count(self):
        return self.posts.count() - 1  # Excluding the initial post

    def latest_reply(self):
        return self.posts.order_by('-created_at').first()


class ForumPost(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Post by {self.author.username} on {self.topic.title}'


class Topic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:forum_topic', kwargs={'slug': self.slug})


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BibleStudy(models.Model):
    STUDY_TYPES = [
        ('general', 'General Bible Study'),
        ('topical', 'Topical Study'),
        ('book', 'Book Study'),
        ('character', 'Character Study'),
        ('youth', 'Youth Bible Study'),
        ('women', 'Women\'s Bible Study'),
        ('men', 'Men\'s Bible Study'),
    ]

    TARGET_GROUPS = [
        ('all', 'All Ages'),
        ('youth', 'Youth (13-18)'),
        ('young_adults', 'Young Adults (19-30)'),
        ('adults', 'Adults (31+)'),
        ('women', 'Women Only'),
        ('men', 'Men Only'),
        ('seniors', 'Seniors (60+)'),
    ]

    RECURRING_PATTERNS = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    study_type = models.CharField(max_length=20, choices=STUDY_TYPES)
    target_group = models.CharField(max_length=20, choices=TARGET_GROUPS, default='')
    description = models.TextField()

    # Schedule
    start_date = models.DateField(default=timezone.now)
    time = models.TimeField(default=time(19, 0))  # 7:00 PM default
    duration = models.DurationField(default=timedelta(hours=1))
    end_date = models.DateField(null=True, blank=True)

    # Location and Capacity
    location = models.CharField(max_length=200)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True, null=True)
    max_participants = models.PositiveIntegerField(default=20)

    # Study Details
    scripture_focus = models.CharField(max_length=200, null=True)
    study_outline = models.TextField(null=True)
    materials = models.FileField(upload_to='bible_studies/materials/', blank=True)

    # Leaders
    leaders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='led_bible_studies')

    # Recurring Settings
    is_recurring = models.BooleanField(default=False)
    recurring_pattern = models.CharField(
        max_length=20,
        choices=RECURRING_PATTERNS,
        blank=True,
        null=True
    )

    # Registration
    registration_required = models.BooleanField(default=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)

    # Status and Metadata
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_bible_studies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'time']
        verbose_name_plural = "Bible Studies"

    def __str__(self):
        return self.title

    @property
    def registered_participants_count(self):
        return self.registrations.count()

    @property
    def spots_available(self):
        return self.max_participants - self.registered_participants_count

    @property
    def is_full(self):
        return self.registered_participants_count >= self.max_participants


class ChildRegistration(models.Model):
    child_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(18)]
    )
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registered_children'
    )
    emergency_contact = models.CharField(max_length=100)
    medical_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Testimony(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    prayer_request = models.ForeignKey(
        'PrayerRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonies'
    )

    class Meta:
        verbose_name_plural = "Testimonies"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Child(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='children'
    )
    allergies = models.TextField(blank=True)
    medical_notes = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=200)
    photo_permission = models.BooleanField(default=False)
    special_needs = models.TextField(blank=True)
    pickup_allowed_by = models.TextField(help_text="Names of people allowed to pick up the child", null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class ChildrensMinistry(models.Model):
    AGE_GROUP_CHOICES = [
        ('2-4', 'Toddlers (2-4)'),
        ('5-7', 'Early Elementary (5-7)'),
        ('8-10', 'Elementary (8-10)'),
        ('11-12', 'Pre-Teens (11-12)')
    ]

    PROGRAM_TYPE_CHOICES = [
        ('SUNDAY_SCHOOL', 'Sunday School'),
        ('BIBLE_CLUB', 'Bible Club'),
        ('VACATION_BIBLE', 'Vacation Bible School'),
        ('CHOIR', 'Children\'s Choir'),
        ('ARTS_CRAFTS', 'Arts & Crafts'),
        ('DRAMA', 'Drama Ministry'),
        ('MISSIONS', 'Kids Missions')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    program_type = models.CharField(max_length=50, choices=PROGRAM_TYPE_CHOICES)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_childrens_ministries'
    )
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teaching_ministries',
        blank=True
    )
    children = models.ManyToManyField(
        'Child',
        related_name='enrolled_programs',
        through='ChildEnrollment'
    )
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='childrens_ministry/', blank=True, null=True)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    curriculum = models.FileField(upload_to='curriculum/', blank=True, null=True)
    safety_guidelines = models.TextField(blank=True)
    allergies_aware = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ChildEnrollment(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    program = models.ForeignKey(ChildrensMinistry, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    attendance_record = models.ManyToManyField(
        'ChildAttendance',
        related_name='enrollments',
        blank=True
    )
    notes = models.TextField(blank=True)

class ChildAttendance(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    program = models.ForeignKey(ChildrensMinistry, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    checked_in_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='checkins_performed'
    )
    checked_out_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='checkouts_performed'
    )
    pickup_person = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)


class NotificationPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_updates = models.BooleanField(default=True)
    email_new_warriors = models.BooleanField(default=True)
    sms_updates = models.BooleanField(default=False)
    sms_new_warriors = models.BooleanField(default=False)
    real_time_notifications = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Notification preferences for {self.user.username}"


class PrayerRequest(models.Model):
    PRAYER_CATEGORIES = [
        ('healing', 'Physical Healing'),
        ('spiritual', 'Spiritual Growth'),
        ('family', 'Family Issues'),
        ('financial', 'Financial Needs'),
        ('guidance', 'Guidance & Direction'),
        ('other', 'Other')
    ]

    PRAYER_STATUS = [
        ('new', 'New Request'),
        ('praying', 'Being Prayed For'),
        ('answered', 'Prayer Answered'),
        ('archived', 'Archived')
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prayer_requests')
    title = models.CharField(max_length=200)
    request = models.TextField()
    category = models.CharField(max_length=20, choices=PRAYER_CATEGORIES)
    is_anonymous = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PRAYER_STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prayer_warriors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='praying_for',
        blank=True
    )
    testimony = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def prayer_count(self):
        return self.prayer_warriors.count()


class PrayerUpdate(models.Model):
    prayer_request = models.ForeignKey(
        PrayerRequest,
        on_delete=models.CASCADE,
        related_name='updates'
    )
    update_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class SmallGroup(models.Model):
    GROUP_TYPES = (
        ('bible_study', 'Bible Study'),
        ('prayer', 'Prayer Group'),
        ('fellowship', 'Fellowship'),
        ('ministry', 'Ministry Team'),
        ('support', 'Support Group'),
        ('discipleship', 'Discipleship'),
        ('outreach', 'Outreach'),
        ('other', 'Other'),
    )

    MEETING_FREQUENCIES = (
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    )

    MEETING_DAYS = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )

    # Basic Information
    name = models.CharField(
        max_length=100,
        help_text="Name of the small group"
    )
    description = models.TextField(
        help_text="Detailed description of the group's purpose and activities"
    )
    group_type = models.CharField(
        max_length=20,
        choices=GROUP_TYPES,
        help_text="Type of small group"
    )
    image = models.ImageField(
        upload_to='small_groups/',
        blank=True,
        null=True,
        help_text="Group photo or image"
    )

    # Members and Leaders
    leaders = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='led_groups',
        help_text="Group leaders"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_groups',
        help_text="Group members"
    )
    max_members = models.PositiveIntegerField(
        validators=[MinValueValidator(2)],
        help_text="Maximum number of members allowed"
    )

    # Meeting Details
    meeting_frequency = models.CharField(
        max_length=20,
        choices=MEETING_FREQUENCIES,
        help_text="How often the group meets"
    )
    meeting_day = models.CharField(
        max_length=20,
        choices=MEETING_DAYS,
        help_text="Day of the week when the group meets"
    )
    meeting_time = models.TimeField(
        help_text="Time when the group meets"
    )
    is_online = models.BooleanField(
        default=False,
        help_text="Whether the group meets online"
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Physical location or online meeting link"
    )

    # Settings
    is_accepting_members = models.BooleanField(
        default=True,
        help_text="Whether the group is currently accepting new members"
    )
    requires_approval = models.BooleanField(
        default=False,
        help_text="Whether new members need approval to join"
    )

    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_groups',
        help_text="User who created the group",
        null=True,  # Allow null for existing records
        default=1
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the group was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the group was last updated"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Small Group'
        verbose_name_plural = 'Small Groups'

    def __str__(self):
        return self.name

    @property
    def is_full(self):
        """Check if the group has reached its maximum capacity"""
        return self.members.count() >= self.max_members

    @property
    def available_spots(self):
        """Calculate number of available spots"""
        return max(0, self.max_members - self.members.count())

    @property
    def member_count(self):
        """Get the current number of members"""
        return self.members.count()

    def can_join(self, user):
        """Check if a user can join the group"""
        return (
                self.is_accepting_members
                and not self.is_full
                and user not in self.members.all()
        )

    def can_leave(self, user):
        """Check if a user can leave the group"""
        if user not in self.members.all():
            return False
        # Don't allow last leader to leave
        if user in self.leaders.all() and self.leaders.count() == 1:
            return False
        return True

    def add_member(self, user):
        """Add a member to the group"""
        if self.can_join(user):
            self.members.add(user)
            return True
        return False

    def remove_member(self, user):
        """Remove a member from the group"""
        if self.can_leave(user):
            self.members.remove(user)
            if user in self.leaders.all():
                self.leaders.remove(user)
            return True
        return False


from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class YouthProgram(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('WORSHIP', 'Worship Team'),
        ('BIBLE_STUDY', 'Bible Study'),
        ('MENTORSHIP', 'Mentorship'),
        ('OUTREACH', 'Outreach'),
        ('SPORTS', 'Sports Ministry'),
        ('ARTS', 'Arts & Music'),
        ('LEADERSHIP', 'Leadership Development'),
    ]

    AGE_GROUP_CHOICES = [
        ('13-15', 'Young Teens (13-15)'),
        ('16-18', 'Older Teens (16-18)'),
        ('19-25', 'Young Adults (19-25)'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    program_type = models.CharField(max_length=50, choices=PROGRAM_TYPE_CHOICES)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_youth_programs'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='youth_program_memberships',
        blank=True
    )
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='youth_programs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    requirements = models.TextField(blank=True)
    parent_consent_required = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate base slug from title
            base_slug = slugify(self.title)
            slug = base_slug

            # Ensure unique slug
            counter = 1
            while YouthProgram.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:youth_program_detail', kwargs={'slug': self.slug})



class YouthEvent(models.Model):
    program = models.ForeignKey(YouthProgram, on_delete=models.CASCADE, related_name='events', null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='youth_events/', blank=True, null=True)
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='YouthEventAttendee',
        related_name='youth_events_attending'
    )
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    permission_slip_required = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.program.title}"

    def is_registration_open(self):
        if not self.registration_deadline:
            return True
        return timezone.now() <= self.registration_deadline

    def has_space(self):
        if not self.max_attendees:
            return True
        return self.attendees.count() < self.max_attendees

    def get_attendee_status(self, user):
        try:
            attendee = YouthEventAttendee.objects.get(event=self, user=user)
            return {
                'is_attending': True,
                'permission_slip_submitted': attendee.permission_slip_submitted,
                'payment_completed': attendee.payment_completed
            }
        except YouthEventAttendee.DoesNotExist:
            return {
                'is_attending': False,
                'permission_slip_submitted': False,
                'payment_completed': False
            }



class YouthMinistry(models.Model):
    EVENT_TYPES = (
        ('fellowship', 'Youth Fellowship'),
        ('worship', 'Youth Worship'),
        ('outreach', 'Youth Outreach'),
        ('camp', 'Youth Camp'),
        ('training', 'Leadership Training'),
    )

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True)
    coordinator = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=200)
    age_range = models.CharField(max_length=50)  # e.g., "13-18"
    leaders = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='youth_events_leading'
    )
    image = models.ImageField(upload_to='youth_ministry/', blank=True, null=True)
    registration_required = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='youth_events',
        blank=True
    )
    is_active = models.BooleanField(default=True)


class ChildrenProgram(models.Model):
    PROGRAM_TYPES = [
        ('sunday_school', 'Sunday School'),
        ('vbs', 'Vacation Bible School'),
        ('camp', 'Children\'s Camp'),
        ('special', 'Special Program'),
    ]

    AGE_GROUPS = [
        ('2-4', 'Toddlers (2-4 years)'),
        ('5-7', 'Early Elementary (5-7 years)'),
        ('8-11', 'Upper Elementary (8-11 years)'),
        ('all', 'All Ages'),
    ]

    RECURRING_PATTERNS = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    ]

    title = models.CharField(max_length=200)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    age_group = models.CharField(max_length=10, choices=AGE_GROUPS)
    max_children = models.PositiveIntegerField()
    description = models.TextField()
    curriculum = models.TextField()
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='children_programs')
    materials_needed = models.TextField(blank=True)
    image = models.ImageField(upload_to='children_programs/', blank=True, null=True)
    registration_deadline = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurring_pattern = models.CharField(max_length=20, choices=RECURRING_PATTERNS, blank=True, null=True)
    parent_instructions = models.TextField(blank=True)
    special_needs_support = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='created_children_programs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return timezone.now() > timezone.make_aware(datetime.combine(self.date, self.time))

    @property
    def registered_children_count(self):
        return self.registrations.count()

    @property
    def spots_available(self):
        return self.max_children - self.registered_children_count


class SongRequest(models.Model):
    OCCASION_CHOICES = [
        ('sunday_service', 'Sunday Service'),
        ('special_event', 'Special Event'),
        ('youth_service', 'Youth Service'),
        ('prayer_meeting', 'Prayer Meeting'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='song_requests')
    song_title = models.CharField(max_length=255, null=True)
    artist = models.CharField(max_length=255, blank=True, null=True)
    preferred_date = models.DateField(null=True, blank=True)
    occasion = models.CharField(max_length=50, choices=OCCASION_CHOICES, null=True)
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_urgent = models.BooleanField(default=False)

    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_song_requests'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.song_title} - Requested by {self.user.username}"

    def get_status_color(self):
        """Return Bootstrap color class based on status"""
        status_colors = {
            'pending': 'warning',
            'approved': 'info',
            'scheduled': 'primary',
            'declined': 'danger',
            'completed': 'success',
        }
        return status_colors.get(self.status, 'secondary')

    def save(self, *args, **kwargs):
        # If status changes to approved/declined, set reviewed_at
        if self.pk:
            old_status = SongRequest.objects.get(pk=self.pk).status
            if old_status != self.status and self.status in ['approved', 'declined']:
                self.reviewed_at = timezone.now()
        super().save(*args, **kwargs)


class Event(models.Model):
    EVENT_TYPES = [
        ('service', 'Church Service'),
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('youth', 'Youth Event'),
        ('children', 'Children Event'),
        ('outreach', 'Outreach'),
        ('prayer', 'Prayer Meeting'),
        ('fellowship', 'Fellowship'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    online_link = models.URLField(null=True)
    is_recurring = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)

    slug = models.SlugField(unique=True)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Date and Time
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(null=True, blank=True)

    # Location
    location = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    date = models.DateTimeField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.DateTimeField(null=True)

    # Capacity and Registration
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    registration_required = models.BooleanField(default=False)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='EventRegistration',
                                          related_name='events_attending')

    # Media
    image = models.ImageField(upload_to='event_images/', null=True)
    banner = models.ImageField(upload_to='event_banners/', null=True, blank=True)
    video_url = models.URLField(blank=True)

    # Organization
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_organized_events'
    )
    ministry = models.ForeignKey('Ministry', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    featured = models.BooleanField(default=False)

    # Additional Info
    schedule = models.TextField(blank=True, help_text="Detailed schedule of the event")
    speakers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='service_speaking_events'
    )
    resources = models.FileField(upload_to='event_resources/', null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date', 'status']),
            models.Index(fields=['event_type']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        return self.end_date < timezone.now()

    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def registration_open(self):
        if not self.registration_required:
            return False
        if not self.registration_deadline:
            return True
        return timezone.now() <= self.registration_deadline

    @property
    def spots_available(self):
        if not self.max_participants:
            return None
        return self.max_participants - self.participants.count()

    @property
    def is_full(self):
        if not self.max_participants:
            return False
        return self.participants.count() >= self.max_participants


class EventRegistration(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)
    attended = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['event', 'participant']
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.participant.username} - {self.event.title}"


class EventFeedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for {self.event.title} by {self.user.username}"


class Ministry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                               related_name='led_ministries')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='ministry_images/', null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ministries"

    def __str__(self):
        return self.name


class VolunteerOpportunity(models.Model):
    FREQUENCY_CHOICES = (
        ('one-time', 'One-Time Event'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('flexible', 'Flexible'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('filled', 'Filled'),
        ('urgent', 'Urgent Need'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    ministry = models.ForeignKey('Ministry', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='volunteer_opportunity')
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requirements = models.TextField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    time_commitment = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    max_volunteers = models.PositiveIntegerField(null=True, blank=True)
    volunteers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='VolunteerSignup',
        through_fields=('opportunity', 'volunteer'),  # Specify the through fields
        related_name='volunteer_opportunities'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('volunteers:opportunity_detail', kwargs={'slug': self.slug})

    @property
    def spots_remaining(self):
        if self.max_volunteers:
            return max(0, self.max_volunteers - self.volunteers.count())
        return None

    @property
    def is_full(self):
        if self.max_volunteers:
            return self.volunteers.count() >= self.max_volunteers
        return False


class VolunteerSignup(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )

    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    signup_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    availability = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_signups'
    )
    approved_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('volunteer', 'opportunity')

    def __str__(self):
        return f"{self.volunteer.get_full_name()} - {self.opportunity.title}"


class MinistryRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'ministry']

    def __str__(self):
        return f"{self.user.username} - {self.ministry.name}"


class SermonCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class name", default="bi-bookmark")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sermon Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def sermons_count(self):
        return self.sermons.count()


class SermonSeries(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='sermon_series/thumbnails/', null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Sermon Series"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Sermon(models.Model):

    sermon_notes = models.FileField(upload_to='sermon_notes/', null=True, blank=True)
    study_materials = models.FileField(upload_to='study_materials/', null=True, blank=True)
    key_points = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    scripture_reference = models.CharField(max_length=200)
    preacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    series = models.ForeignKey(
        'SermonSeries',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sermons'
    )
    date_preached = models.DateField()
    video_file = models.FileField(
        upload_to='sermons/videos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['mp4', 'webm'])]
    )
    audio_file = models.FileField(
        upload_to='sermons/audio/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['mp3', 'wav'])]
    )
    presentation_slides = models.FileField(
        upload_to='sermons/slides/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'pptx'])]
    )
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', null=True)
    duration = models.DurationField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('SermonTag', blank=True)
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_preached']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SermonTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class SermonComment(models.Model):
    sermon = models.ForeignKey('Sermon', on_delete=models.CASCADE, related_name='sermon_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.sermon.title}'


class SermonNote(models.Model):
    sermon = models.ForeignKey('Sermon', on_delete=models.CASCADE, related_name='user_notes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DurationField()  # Point in the sermon where note was taken
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['timestamp']


class Channel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'channel')

    def __str__(self):
        return f'{self.subscriber} -> {self.channel.name}'


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('reply', 'Reply to Topic'),
        ('mention', 'Mention in Post'),
        ('like', 'Post Like'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']


class MarriageMinistry(models.Model):
    MEETING_TYPE_CHOICES = [
        ('in_person', 'In Person'),
        ('virtual', 'Virtual'),
        ('hybrid', 'Hybrid')
    ]

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = SummernoteTextField()
    start_date = models.DateField()
    end_date = models.DateField()
    meeting_time = models.TimeField()
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE_CHOICES)
    location = models.CharField(max_length=255, blank=True)
    zoom_link = models.URLField(blank=True)
    max_couples = models.PositiveIntegerField(default=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    facilitators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='facilitated_programs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Marriage Ministries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:marriage_program_detail', kwargs={'slug': self.slug})


class CoupleProfile(models.Model):
    MARRIAGE_STAGE_CHOICES = [
        ('NEWLYWED', 'Newlywed (0-2 years)'),
        ('EARLY', 'Early Years (3-7 years)'),
        ('ESTABLISHED', 'Established (8-15 years)'),
        ('SEASONED', 'Seasoned (15+ years)'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('EMAIL', 'Email'),
        ('PHONE', 'Phone'),
        ('BOTH', 'Both Email and Phone'),
    ]

    # Primary user (the one who created the profile)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='couple_profile', null=True)

    # Partner Information
    partner_name = models.CharField(max_length=100, null=True)
    partner_email = models.EmailField(null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    partner_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Relationship Details
    anniversary = models.DateField(default=timezone.now)
    marriage_stage = models.CharField(
        max_length=20,
        choices=MARRIAGE_STAGE_CHOICES,
        default='NEWLYWED'
    )

    # Profile Details
    profile_image = models.ImageField(upload_to='couple_profiles/', blank=True, null=True)
    about_us = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    # Contact Preferences
    preferred_contact_method = models.CharField(
        max_length=5,
        choices=CONTACT_METHOD_CHOICES,
        default='EMAIL'
    )

    # Privacy Settings
    is_public = models.BooleanField(default=False)
    show_anniversary = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        # Add only these new fields for approval system
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_couple_profiles'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Approval'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    rejection_reason = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'approved' and not self.is_approved:
            self.is_approved = True
            self.approval_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_username()}'s Couple Profile"

    def get_couple_name(self):
        return f"{self.user.get_username()} & {self.partner_name}"


class MarriageEnrollment(models.Model):
    program = models.ForeignKey(MarriageMinistry, on_delete=models.CASCADE)
    # couple = models.ForeignKey(CoupleProfile, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['program', ]


class MarriageResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('podcast', 'Podcast'),
        ('worksheet', 'Worksheet')
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    description = models.TextField()
    content = SummernoteTextField(blank=True)
    file = models.FileField(upload_to='marriage_resources/', blank=True)
    external_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MarriageCounseling(models.Model):
    # couple = models.ForeignKey(CoupleProfile, on_delete=models.CASCADE)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    meeting_type = models.CharField(max_length=20, choices=MarriageMinistry.MEETING_TYPE_CHOICES)
    status = models.CharField(max_length=20, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preferred_date = models.DateField(auto_now=True)
    is_urgent = models.BooleanField(default=True)
    reason = models.TextField(null=True, blank=True)



class MarriageEvent(models.Model):
    title = models.CharField(max_length=200)
    description = SummernoteTextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    max_participants = models.PositiveIntegerField(default=20)
    registration_deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class FamilyGroup(models.Model):
    name = models.CharField(max_length=200)
    description = SummernoteTextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='family_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FamilyEvent(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('retreat', 'Retreat'),
        ('activity', 'Family Activity'),
        ('support', 'Support Group')
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = SummernoteTextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    virtual_link = models.URLField(blank=True)
    max_participants = models.PositiveIntegerField(default=20)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='family_events_attending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ParentingResource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('podcast', 'Podcast'),
        ('guide', 'Parenting Guide'),
        ('activity', 'Family Activity')
    ]

    AGE_GROUPS = [
        ('infant', '0-2 years'),
        ('toddler', '2-4 years'),
        ('preschool', '4-6 years'),
        ('school', '6-12 years'),
        ('teen', '13-19 years'),
        ('all', 'All Ages')
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS)
    description = models.TextField()
    content = SummernoteTextField(blank=True)
    file = models.FileField(upload_to='family_resources/', blank=True)
    external_link = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class CoupleProfile(models.Model):
        MARRIAGE_STAGE_CHOICES = [
            ('NEWLYWED', 'Newlywed (0-2 years)'),
            ('EARLY', 'Early Years (3-7 years)'),
            ('ESTABLISHED', 'Established (8-15 years)'),
            ('SEASONED', 'Seasoned (15+ years)'),
        ]

        # ... existing fields ...

        # Add these fields for reading streak
        reading_streak = models.IntegerField(default=0)
        last_reading_date = models.DateField(null=True, blank=True)

        def update_reading_streak(self):
            today = timezone.now().date()
            if self.last_reading_date == today - timezone.timedelta(days=1):
                self.reading_streak += 1
            elif self.last_reading_date != today:
                self.reading_streak = 1
            self.last_reading_date = today
            self.save()


class FamilyCounseling(models.Model):
    COUNSELING_TYPES = [
        ('parenting', 'Parenting Guidance'),
        ('relationship', 'Family Relationships'),
        ('crisis', 'Crisis Intervention'),
        ('grief', 'Grief Support'),
        ('general', 'General Family Support')
    ]

    family = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    counseling_type = models.CharField(max_length=20, choices=COUNSELING_TYPES)
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='family_counseling_sessions',
        on_delete=models.CASCADE
    )
    scheduled_time = models.DateTimeField()
    notes = models.TextField(blank=True)
    is_virtual = models.BooleanField(default=False)
    zoom_link = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='scheduled'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class FamilyDiscussion(models.Model):
    title = models.CharField(max_length=200)
    content = SummernoteTextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_family_discussions'
    )
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:family_discussion_detail', kwargs={'slug': self.slug})


class DiscussionComment(models.Model):
    discussion = models.ForeignKey(
        FamilyDiscussion,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NewBelieverProfile(models.Model):
    FAITH_STAGES = [
        ('new', 'New to Faith'),
        ('growing', 'Growing in Faith'),
        ('maturing', 'Maturing Believer'),
        ('discipling', 'Discipling Others')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='new_believer_profile')
    date_joined = models.DateField(auto_now_add=True, null=True)
    faith_stage = models.CharField(max_length=20, choices=FAITH_STAGES, default='new')
    testimony = models.TextField(blank=True)
    baptism_status = models.BooleanField(default=False)
    baptism_date = models.DateField(null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentees')
    reading_streak = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='believer_avatars/', null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_believer_profiles'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Approval'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    rejection_reason = models.TextField(blank=True)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()

            # Show appropriate messages based on profile status
            if self.object.status == 'pending':
                messages.info(request, 'Your profile is pending approval from the admin.')
            elif self.object.status == 'rejected':
                messages.warning(request, f'Your profile was rejected. Reason: {self.object.rejection_reason}')

            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        except CoupleProfile.DoesNotExist:
            messages.warning(request, 'Please create your couple profile first.')
            return redirect('services:create_couple_profile')

    def get_object(self):
        return get_object_or_404(CoupleProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        # Calculate marriage duration
        marriage_duration = timezone.now().date() - profile.anniversary
        years = marriage_duration.days // 365
        months = (marriage_duration.days % 365) // 30

        # Get activity statistics
        context.update({
            # Profile Status
            'profile_status': {
                'status': profile.get_status_display(),
                'is_approved': profile.is_approved,
                'approval_date': profile.approval_date,
                'approved_by': profile.approved_by,
                'rejection_reason': profile.rejection_reason if profile.status == 'rejected' else None,
            },

            # Marriage Info
            'marriage_info': {
                'duration_years': years,
                'duration_months': months,
                'stage': profile.get_marriage_stage_display(),
            },

            # Activity Summary
            'reading_plans': BibleReadingPlan.objects.filter(couples=profile).annotate(
                completion_percentage=models.F('completed_chapters') * 100.0 / models.F('total_chapters')
            )[:3],

            'upcoming_events': CoupleEvent.objects.filter(
                couples=profile,
                date__gte=timezone.now()
            ).order_by('date')[:3],

            'recent_prayers': PrayerRequest.objects.filter(
                couple=profile
            ).order_by('-created_at')[:3],

            # Statistics
            'statistics': {
                'total_events': CoupleEvent.objects.filter(couples=profile).count(),
                'reading_streak': profile.reading_streak,
                'prayer_requests': PrayerRequest.objects.filter(couple=profile).count(),
                'answered_prayers': PrayerRequest.objects.filter(
                    couple=profile,
                    status='answered'
                ).count(),
            },
        })
        return context

    def save(self, *args, **kwargs):
        if self.status == 'approved' and not self.is_approved:
            self.is_approved = True
            self.approval_date = timezone.now()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.user.get_full_name()

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('images/default_avatar.png')

    class Meta:
        ordering = ['-date_joined']


class DiscipleshipTrack(models.Model):
    title = models.CharField(max_length=200)
    description = SummernoteTextField()
    duration_weeks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class CoupleProfile(models.Model):
        MARRIAGE_STAGE_CHOICES = [
            ('NEWLYWED', 'Newlywed (0-2 years)'),
            ('EARLY', 'Early Years (3-7 years)'),
            ('ESTABLISHED', 'Established (8-15 years)'),
            ('SEASONED', 'Seasoned (15+ years)'),
        ]

        CONTACT_METHOD_CHOICES = [
            ('EMAIL', 'Email'),
            ('PHONE', 'Phone'),
            ('BOTH', 'Both Email and Phone'),
        ]

        # Primary user (the one who created the profile)
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='couple_profile', null=True)

        # Partner Information
        partner_name = models.CharField(max_length=100, null=True, blank=True)
        partner_email = models.EmailField(null=True, blank=True)
        partner_phone = models.CharField(max_length=15, blank=True)

        # Relationship Details
        anniversary = models.DateField()
        marriage_stage = models.CharField(
            max_length=20,
            choices=MARRIAGE_STAGE_CHOICES,
            default='NEWLYWED'
        )

        # Profile Details
        profile_image = models.ImageField(upload_to='couple_profiles/', blank=True, null=True)
        about_us = models.TextField(blank=True)
        interests = models.TextField(blank=True)

        # Contact Preferences
        preferred_contact_method = models.CharField(
            max_length=5,
            choices=CONTACT_METHOD_CHOICES,
            default='EMAIL'
        )

        # Privacy Settings
        is_public = models.BooleanField(default=False)
        show_anniversary = models.BooleanField(default=True)

        # Reading Streak
        reading_streak = models.IntegerField(default=0)
        last_reading_date = models.DateField(null=True, blank=True)

        # Approval System
        is_approved = models.BooleanField(default=False)
        approval_date = models.DateTimeField(null=True, blank=True)
        approved_by = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='approved_profiles'
        )
        status = models.CharField(
            max_length=20,
            choices=[
                ('pending', 'Pending Approval'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'),
            ],
            default='pending'
        )
        rejection_reason = models.TextField(blank=True)

        # Metadata
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"{self.user.get_full_name()}'s Couple Profile"

        def get_couple_name(self):
            return f"{self.user.username()} & {self.partner_name}"

        def update_reading_streak(self):
            today = timezone.now().date()
            if self.last_reading_date == today - timezone.timedelta(days=1):
                self.reading_streak += 1
            elif self.last_reading_date != today:
                self.reading_streak = 1
            self.last_reading_date = today
            self.save()

        def save(self, *args, **kwargs):
            if self.status == 'approved' and not self.is_approved:
                self.is_approved = True
                self.approval_date = timezone.now()
            super().save(*args, **kwargs)


class DiscipleshipModule(models.Model):
    track = models.ForeignKey(DiscipleshipTrack, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = SummernoteTextField()
    order = models.PositiveIntegerField()
    video_url = models.URLField(blank=True)
    resources = models.FileField(upload_to='discipleship/resources/', blank=True)
    completion_time = models.DurationField()

    class Meta:
        ordering = ['order']


class BelieverProgress(models.Model):
    believer = models.ForeignKey(NewBelieverProfile, on_delete=models.CASCADE)
    module = models.ForeignKey(DiscipleshipModule, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['believer', 'module']


class MentorshipSession(models.Model):
    SESSION_TYPES = [
        ('in_person', 'In-Person Meeting'),
        ('virtual', 'Virtual Meeting'),
        ('phone', 'Phone Call')
    ]

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentor_sessions'
    )
    mentee = models.ForeignKey(
        NewBelieverProfile,
        on_delete=models.CASCADE,
        related_name='mentee_sessions'
    )
    scheduled_time = models.DateTimeField()
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)


class PrayerJournal(models.Model):
    believer = models.ForeignKey(NewBelieverProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answered = models.BooleanField(default=False)
    answer_date = models.DateField(null=True, blank=True)
    answer_notes = models.TextField(blank=True)


class BibleReadingPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('DAILY', 'Daily Reading'),
        ('WEEKLY', 'Weekly Study'),
        ('TOPICAL', 'Topical Study'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES, null=True)
    # Changed from couple to couples to match your existing naming convention
    couples = models.ManyToManyField('CoupleProfile', related_name='reading_plans')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    total_chapters = models.IntegerField(default=0)
    completed_chapters = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return self.title

    @property
    def progress(self):
        if self.total_chapters == 0:
            return 0
        return (self.completed_chapters / self.total_chapters) * 100

class BibleReading(models.Model):
    plan = models.ForeignKey(BibleReadingPlan, on_delete=models.CASCADE, null=True)
    day_number = models.PositiveIntegerField()
    scripture_reference = models.CharField(max_length=100)
    devotional = models.TextField()
    reflection_questions = models.TextField()


class ReadingProgress(models.Model):
    believer = models.ForeignKey(NewBelieverProfile, on_delete=models.CASCADE)
    reading = models.ForeignKey(BibleReading, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    reflection = models.TextField(blank=True)

    class Meta:
        unique_together = ['believer', 'reading']


class CoupleEvent(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('retreat', 'Retreat'),
        ('counseling', 'Counseling Session'),
        ('social', 'Social Gathering'),
        ('prayer', 'Prayer Meeting')
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = SummernoteTextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    virtual_meeting_link = models.URLField(blank=True)
    max_couples = models.PositiveIntegerField()
    registration_deadline = models.DateField(default=timezone.now)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class CounselingSession(models.Model):
    SESSION_TYPES = [
        ('initial', 'Initial Consultation'),
        ('followup', 'Follow-up Session'),
        ('crisis', 'Crisis Intervention'),
        ('premarital', 'Pre-marital Counseling'),
        ('reconciliation', 'Reconciliation Session')
    ]

    couple = models.ForeignKey(CoupleProfile, on_delete=models.CASCADE)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    scheduled_time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    virtual_meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    homework_assigned = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    followup_needed = models.BooleanField(default=False)
    private_notes = models.TextField(blank=True)  # For counselor's eyes only


class CoupleResource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('worksheet', 'Worksheet'),
        ('podcast', 'Podcast')
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = SummernoteTextField()
    content = SummernoteTextField(blank=True)  # For articles
    file = models.FileField(upload_to='couple_resources/', blank=True)
    external_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200, blank=True)  # Comma-separated tags
    featured = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)


class CoupleJournal(models.Model):
    couple = models.ForeignKey(CoupleProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = SummernoteTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    mood_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    shared_with_counselor = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)


class DateNightIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    location_type = models.CharField(max_length=50)  # indoor/outdoor/virtual
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CoupleProfile, related_name='liked_ideas')
    tried = models.ManyToManyField(CoupleProfile, related_name='tried_ideas')


class CouplePrayerRequest(models.Model):
    couple = models.ForeignKey(CoupleProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    request = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_answered = models.BooleanField(default=False)
    answer_date = models.DateField(null=True, blank=True)
    answer_testimony = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Prayer Request from {self.couple} - {self.title}"


class WatchedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('videos.Content', on_delete=models.CASCADE)
    watch_duration = models.DurationField()
    completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'video']


class DownloadedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(
        'videos.Content',
        on_delete=models.CASCADE,
        related_name='service_downloaded_videos'
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'video']


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CounselingRequest(models.Model):
    REASON_CHOICES = [
        ('PREMARITAL', 'Premarital Counseling'),
        ('MARRIAGE', 'Marriage Counseling'),
        ('CONFLICT', 'Conflict Resolution'),
        ('SPIRITUAL', 'Spiritual Growth'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    couple = models.ForeignKey('CoupleProfile', on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    additional_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='counseling_sessions'
    )
    scheduled_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Counseling Request - {self.couple.get_couple_name()}"

    class Meta:
        ordering = ['-created_at']


class MensMinistry(models.Model):
    MINISTRY_TYPE_CHOICES = [
        ('BIBLE_STUDY', 'Bible Study'),
        ('DISCIPLESHIP', 'Discipleship'),
        ('MENTORSHIP', 'Mentorship'),
        ('OUTREACH', 'Outreach'),
        ('LEADERSHIP', 'Leadership'),
        ('FELLOWSHIP', 'Fellowship'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_mens_ministries'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='mens_ministry_memberships',
        blank=True
    )
    ministry_type = models.CharField(max_length=50, choices=MINISTRY_TYPE_CHOICES)
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='mens_ministry/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Men's Ministries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:mens_ministry_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class MensEvent(models.Model):
    ministry = models.ForeignKey(MensMinistry, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='mens_ministry_events',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='mens_events/', blank=True, null=True)
    event_type = models.CharField(max_length=50, choices=MensMinistry.MINISTRY_TYPE_CHOICES)
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.ministry.title}"

    def is_registration_open(self):
        if not self.registration_deadline:
            return True
        return timezone.now() <= self.registration_deadline

    def has_space(self):
        if not self.max_attendees:
            return True
        return self.attendees.count() < self.max_attendees



class YouthEventAttendee(models.Model):
    event = models.ForeignKey('YouthEvent', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    permission_slip_submitted = models.BooleanField(default=False)
    payment_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['event', 'user']

class YouthEventPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded')
    ]

    attendee = models.ForeignKey(YouthEventAttendee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Payment for {self.attendee.event.title} - {self.attendee.user.get_full_name()}"

class PermissionSlip(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    attendee = models.ForeignKey(YouthEventAttendee, on_delete=models.CASCADE)
    document = models.FileField(upload_to='permission_slips/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_permission_slips'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Permission Slip for {self.attendee.event.title} - {self.attendee.user.get_full_name()}"

class AttendanceRecord(models.Model):
    event = models.ForeignKey(YouthEvent, on_delete=models.CASCADE)
    attendee = models.ForeignKey(YouthEventAttendee, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['event', 'attendee']

    def __str__(self):
        return f"Attendance for {self.event.title} - {self.attendee.user.get_full_name()}"



class SeniorsMinistry(models.Model):
    ACTIVITY_CHOICES = [
        ('BIBLE_STUDY', 'Bible Study'),
        ('FELLOWSHIP', 'Fellowship Gathering'),
        ('PRAYER', 'Prayer Meeting'),
        ('OUTREACH', 'Community Outreach'),
        ('VISITATION', 'Home Visitation'),
        ('WORKSHOP', 'Life Skills Workshop'),
        ('HEALTH', 'Health & Wellness'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_seniors_ministries'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='seniors_memberships',
        blank=True
    )
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='seniors_ministry/', blank=True, null=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    transportation_provided = models.BooleanField(default=False)
    accessibility_notes = models.TextField(blank=True)
    health_guidelines = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services:seniors_ministry_detail', kwargs={'slug': self.slug})


class SeniorsEvent(models.Model):
    ACTIVITY_CHOICES = [
        ('BIBLE_STUDY', 'Bible Study'),
        ('FELLOWSHIP', 'Fellowship Gathering'),
        ('PRAYER', 'Prayer Meeting'),
        ('OUTREACH', 'Community Outreach'),
        ('VISITATION', 'Home Visitation'),
        ('WORKSHOP', 'Life Skills Workshop'),
        ('HEALTH', 'Health & Wellness'),
    ]
    ministry = models.CharField(max_length=100, choices=ACTIVITY_CHOICES, default='BIBLE_STUDY')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='seniors_events/', blank=True, null=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    transportation_provided = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='seniors_events_attending')

    def __str__(self):
        return self.title

    def has_space(self):
        if not self.max_participants:
            return True
        return self.attendees.count() < self.max_participants

    def is_registration_open(self):
        return timezone.now() <= self.registration_deadline

class TransportationRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ]

    activity = models.ForeignKey(SeniorsMinistry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pickup_address = models.CharField(max_length=255)
    special_needs = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100)
    preferred_pickup_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PrayerPartner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prayer_partnerships')
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prayer_partners')
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class HealthResource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    document = models.FileField(upload_to='seniors_health_resources/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class PrayerPartner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prayer_partnerships')
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prayer_partners')
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)  # Add this field

    class Meta:
        unique_together = ['user', 'partner']

    def __str__(self):
        return f"{self.user} - {self.partner} Prayer Partnership"


class SinglesMinistry(models.Model):
    ACTIVITY_CHOICES = [
        ('BIBLE_STUDY', 'Bible Study'),
        ('FELLOWSHIP', 'Fellowship Group'),
        ('PRAYER', 'Prayer Meeting'),
        ('SOCIAL', 'Social Event'),
        ('WORKSHOP', 'Life Skills Workshop'),
        ('MENTORSHIP', 'Mentorship Program'),
        ('OUTREACH', 'Community Outreach'),
    ]

    RELATIONSHIP_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]

    AGE_GROUP_CHOICES = [
        ('18-25', '18-25 years'),
        ('26-35', '26-35 years'),
        ('36-45', '36-45 years'),
        ('46+', '46+ years'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_singles_ministries'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='singles_memberships',
        blank=True
    )
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='singles_ministry/', blank=True, null=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)
    relationship_status = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_STATUS_CHOICES,
        blank=True
    )
    guidelines = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Singles Ministries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:singles_ministry_detail', kwargs={'slug': self.slug})

    def has_space(self):
        if not self.max_participants:
            return True
        return self.members.count() < self.max_participants

    def __str__(self):
        return self.title

class SinglesEvent(models.Model):
    ministry = models.ForeignKey(
        SinglesMinistry,
        on_delete=models.CASCADE,
        related_name='events'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='singles_events/', blank=True, null=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='singles_events_attending'
    )
    is_couples_allowed = models.BooleanField(default=False)
    event_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    dress_code = models.CharField(max_length=200, blank=True)
    special_instructions = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def has_space(self):
        if not self.max_participants:
            return True
        return self.attendees.count() < self.max_participants

    def is_registration_open(self):
        return timezone.now() <= self.registration_deadline

class MentorshipRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('MATCHED', 'Matched'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ]

    mentee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentorship_requests'
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentor_requests',
        null=True,
        blank=True
    )
    areas_of_focus = models.TextField()
    preferred_meeting_times = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Mentorship Request - {self.mentee.get_full_name()}"

class SinglesResource(models.Model):
    CATEGORY_CHOICES = [
        ('RELATIONSHIP', 'Relationship Advice'),
        ('SPIRITUAL', 'Spiritual Growth'),
        ('CAREER', 'Career Development'),
        ('PERSONAL', 'Personal Development'),
        ('DATING', 'Dating Guidelines'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()
    document = models.FileField(
        upload_to='singles_resources/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
