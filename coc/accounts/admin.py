from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from packaging.utils import _

from .models import *


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # Prevent deletion from User admin
    verbose_name_plural = 'profiles'
    fk_name = 'user'

# Extend the UserAdmin to include Profile information


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'location', 'receive_newsletter', 'bio', 'school_affiliate', 'national_identification_number',
    'country_of_origin', 'current_country_or_residence', 'current_county', 'current_city', 'level_of_education',)
    list_editable = ('receive_newsletter',)  # Make checkbox editable directly in the list view

admin.site.register(UserProfile, ProfileAdmin)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "date_of_birth", "is_active", "is_admin"]


class ChurchUserAdmin(UserAdmin):
    """Admin configuration for the ChurchUser model"""
    # Define fieldsets for the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Define fieldsets for the change form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Contact Information'), {
            'fields': ('phone_number', 'secondary_email')
        }),
        (_('Personal Information'), {
            'fields': ('gender', 'date_of_birth', 'profile_picture')
        }),
        (_('Address'), {
            'fields': ('street_address', 'city', 'state', 'zip_code', 'country')
        }),
        (_('Church Membership'), {
            'fields': ('membership_status', 'membership_date', 'baptism_date')
        }),
        (_('Family Information'), {
            'fields': ('marital_status', 'spouse_name', 'family_id')
        }),
        (_('Emergency Contact'), {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        (_('Privacy Settings'), {
            'fields': ('show_email', 'show_phone', 'show_address')
        }),
        (_('Communication Preferences'), {
            'fields': ('email_opt_in', 'sms_opt_in')
        }),
        (_('Church Attendance'), {
            'fields': ('last_attendance_date', 'notes')
        }),
    )

    # Define which fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'membership_status')

    # Define which fields to use for filtering in the list view
    list_filter = ('is_active', 'membership_status', 'marital_status')

    # Define which fields to use for searching
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    # Define which fields to use in the filter_horizontal widget
    filter_horizontal = ('ministry_interests', 'spiritual_gifts', 'volunteer_availability')

    # Define which fields to order by
    ordering = ('username',)



# Now register the new UserAdmin...
admin.site.register(User, ChurchUserAdmin)
# admin.site.register(UserProfile, ProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
admin.site.unregister(Group)
# admin.site.register(Notifications)
admin.site.register(Report)
admin.site.register(RevenueSharingRule)
# admin.site.register(Subscription)