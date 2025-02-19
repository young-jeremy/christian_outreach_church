from django.conf import settings
# from videos.models import *
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from services.models import Channel
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


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
    google_username = models.CharField(max_length=255, blank=True, null=True)
    google_picture = models.URLField(blank=True, null=True)
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


    def should_notify(self, notification_type):
        if notification_type == 'send_notification_email':
            return self.send_notification_email

    def __str__(self):
        # Example for the User model or Profile model
        return self.username if self.username else "Anonymous"

    def get_all_permissions(self, perm, obj=None):
        return True


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

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


class UserProfile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('regular_account', 'Regular Account'),
        ('premium_account', 'Premium Account'),
        ('business_account', 'Business Account'),
    ]

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
    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    level_of_education = models.CharField(max_length=100, blank=True)

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



