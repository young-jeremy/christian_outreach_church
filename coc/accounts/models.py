# from videos.models import *
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from notifications.models import NotificationSettings
from services.models import Channel
# accounts/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator




class MemberProfile(models.Model):
    MARITAL_STATUS_CHOICES = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
    )

    MEMBERSHIP_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('visitor', 'Visitor'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    profile_image = models.ImageField(upload_to='member_profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)
    address = models.TextField(blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    baptism_date = models.DateField(null=True, blank=True)
    membership_date = models.DateField(null=True, blank=True)
    membership_status = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_STATUS_CHOICES,
        default='visitor'
    )
    skills = models.ManyToManyField('Skill', blank=True)
    ministries = models.ManyToManyField('Ministry', blank=True)
    bio = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = PhoneNumberField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.first_name}-{self.user.last_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Ministry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ministries"



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    google_username = models.CharField(max_length=255, blank=True, null=True)
    google_picture = models.URLField(blank=True, null=True)
    secondary_email = models.EmailField(_('secondary email address'), blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # Address Information
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='United States', blank=True)

    # Church Membership Information
    MEMBERSHIP_STATUS_CHOICES = [
        ('visitor', 'Visitor'),
        ('regular', 'Regular Attendee'),
        ('member', 'Member'),
        ('leader', 'Ministry Leader'),
        ('staff', 'Staff'),
        ('pastor', 'Pastor'),
        ('elder', 'Elder')
    ]
    membership_status = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_STATUS_CHOICES,
        default='visitor'
    )
    membership_date = models.DateField(null=True, blank=True)
    baptism_date = models.DateField(null=True, blank=True)

    # Family Information
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('other', 'Other')
    ]
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True
    )
    spouse_name = models.CharField(max_length=100, blank=True)
    family_id = models.CharField(max_length=50, blank=True, help_text="ID to link family members")

    # Ministry Involvement
    ministry_interests = models.ManyToManyField(
        'Ministry',
        related_name='interested_users',
        blank=True
    )
    spiritual_gifts = models.ManyToManyField(
        'SpiritualGift',
        related_name='gifted_users',
        blank=True
    )
    volunteer_availability = models.ManyToManyField(
        'VolunteerTimeSlot',
        related_name='available_users',
        blank=True
    )

    # Communication Preferences
    email_opt_in = models.BooleanField(default=True)
    sms_opt_in = models.BooleanField(default=False)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)

    # Privacy Settings
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    show_address = models.BooleanField(default=False)

    # Timestamps and Metadata
    last_attendance_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)


    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_joined = models.DateField(auto_now=True, blank=True, null=True)
    send_notification_email = models.BooleanField(default=True)





    objects = MyUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _('church user')
        verbose_name_plural = _('church users')


    def should_notify(self, notification_type):
        if notification_type == 'send_notification_email':
            return self.send_notification_email

    def get_all_permissions(self, perm, obj=None):
        return True


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        return True

    def is_superuser(self, user):
        return user.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def first_name(self):
        return self.first_name()

    def last_name(self):
        return self.last_name()

    def get_full_name(self):
        return self.first_name() + " " + self.last_name()

    def __str__(self):
        return self.username

    def get_age(self):
        """Calculate age based on date of birth"""
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None



class UserProfile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('regular_account', 'Regular Account'),
        ('premium_account', 'Premium Account'),
        ('business_account', 'Business Account'),
    ]
    MINISTRY_CHOICES = [
        ('', 'Select a ministry'),
        ('worship', 'Worship Team'),
        ('youth', 'Youth Ministry'),
        ('children', 'Children\'s Ministry'),
        ('outreach', 'Outreach & Missions'),
        ('prayer', 'Prayer Team'),
        ('admin', 'Administration'),
    ]

    phone = models.CharField(max_length=20, blank=True, null=True)
    ministry = models.CharField(max_length=20, choices=MINISTRY_CHOICES, blank=True)

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    school_affiliate = models.CharField(max_length=100, blank=True)
    national_identification_number = models.IntegerField(blank=True, null=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    course_of_study = models.CharField(max_length=100, blank=True, null=True)
    current_country_or_residence = models.CharField(max_length=100, blank=True)
    current_county = models.CharField(max_length=100, blank=True)
    current_city = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    level_of_education = models.CharField(max_length=100, blank=True)

    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=20, blank=True)

    # Stripe-specific fields
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.ImageField(upload_to='avatars/', default='static/img/undraw_profile_2.svg')
    slug = models.SlugField(unique=True, blank=True)
    receive_newsletter = models.BooleanField(default=False)
    account_type = models.CharField(
        max_length=100,
        choices=ACCOUNT_TYPE_CHOICES,
        default='regular_account'
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    send_notification_email = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.email}'s Profile" if self.user.email else "Unnamed Profile"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from email if username is not available
            base_slug = slugify(self.user.email.split('@')[0])
            if not UserProfile.objects.filter(slug=base_slug).exists():
                self.slug = base_slug
            else:
                counter = 1
                while UserProfile.objects.filter(slug=f"{base_slug}-{counter}").exists():
                    counter += 1
                self.slug = f"{base_slug}-{counter}"

        # Set first_name and last_name if they're empty
        if not self.first_name and self.user.first_name:
            self.first_name = self.user.first_name
        if not self.last_name and self.user.last_name:
            self.last_name = self.user.last_name

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        """Return the user's full name or email if name is not set"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.email.split('@')[0]

    @property
    def display_name(self):
        """Return the name to display in the UI"""
        return self.full_name or self.user.username or self.user.email.split('@')[0]


class ProfileType(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


    def __str__(self):
        return self.profile


class RevenueSharingRule(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    percentage_share = models.DecimalField(max_digits=5, decimal_places=2)


class Report (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_type)


class UserSettings(models.Model):
    """User settings model"""
    BIBLE_CHOICES = [
        ('niv', 'New International Version (NIV)'),
        ('kjv', 'King James Version (KJV)'),
        ('nlt', 'New Living Translation (NLT)'),
        ('esv', 'English Standard Version (ESV)'),
        ('nkjv', 'New King James Version (NKJV)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    show_bible_verses = models.BooleanField(default=True)
    show_prayer_requests = models.BooleanField(default=True)
    show_events = models.BooleanField(default=True)
    preferred_bible = models.CharField(max_length=10, choices=BIBLE_CHOICES, default='niv')

    def __str__(self):
        return f"{self.user.username}'s Settings"


class PrivacySettings(models.Model):
    """User privacy settings model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='privacy')
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    show_address = models.BooleanField(default=False)
    show_prayers = models.BooleanField(default=True)
    show_events = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Privacy Settings"


class MinistryPreferences(models.Model):
    """User ministry preferences model"""
    SPIRITUAL_GIFTS_CHOICES = [
        ('teaching', 'Teaching'),
        ('worship', 'Worship/Music'),
        ('service', 'Service'),
        ('leadership', 'Leadership'),
        ('encouragement', 'Encouragement'),
        ('giving', 'Giving'),
        ('mercy', 'Mercy'),
        ('hospitality', 'Hospitality'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ministry_preferences')
    worship_team = models.BooleanField(default=False)
    children_ministry = models.BooleanField(default=False)
    youth_ministry = models.BooleanField(default=False)
    outreach_ministry = models.BooleanField(default=False)
    prayer_team = models.BooleanField(default=False)
    hospitality_team = models.BooleanField(default=False)

    sunday_morning = models.BooleanField(default=False)
    sunday_evening = models.BooleanField(default=False)
    weekdays = models.BooleanField(default=False)
    special_events = models.BooleanField(default=False)

    spiritual_gifts = MultiSelectField(choices=SPIRITUAL_GIFTS_CHOICES, max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Ministry Preferences"


class ContentSettings(models.Model):
    """User content settings model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='content_settings')
    show_sermons = models.BooleanField(default=True)
    show_devotionals = models.BooleanField(default=True)
    show_bible_studies = models.BooleanField(default=True)
    show_community_posts = models.BooleanField(default=True)
    agree_guidelines = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Content Settings"


class SpiritualGift(models.Model):
    """Spiritual gifts that users can have"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class VolunteerTimeSlot(models.Model):
    """Time slots when users are available to volunteer"""
    DAY_CHOICES = [
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday')
    ]

    TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening')
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time = models.CharField(max_length=10, choices=TIME_CHOICES)

    def __str__(self):
        return f"{self.get_day_display()} {self.get_time_display()}"

    class Meta:
        unique_together = ('day', 'time')
