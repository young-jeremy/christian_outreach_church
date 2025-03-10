from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from .models import *
from django import forms
# from .models import Community
from django.contrib.auth import authenticate
from django.conf import settings
from .admin import *
from .models import *
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm, AuthenticationForm
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import MemberProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile, UserSettings, PrivacySettings, MinistryPreferences, ContentSettings


class PrivacySettingsForm(forms.ModelForm):
    """Form for updating privacy settings"""

    class Meta:
        model = PrivacySettings
        fields = ['show_email', 'show_phone', 'show_address', 'show_prayers', 'show_events']
        widgets = {
            'show_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_phone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_address': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_prayers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_events': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserSettingsForm(forms.ModelForm):
    """Form for updating user settings"""

    class Meta:
        model = UserSettings
        fields = ['show_bible_verses', 'show_prayer_requests', 'show_events', 'preferred_bible']
        widgets = {
            'preferred_bible': forms.Select(attrs={'class': 'form-select'}),
        }


class SecuritySettingsForm(PasswordChangeForm):
    """Form for updating security settings"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class PrivacyForm(forms.ModelForm):
    """Form for updating privacy settings"""

    class Meta:
        model = PrivacySettings
        fields = ['show_email', 'show_phone', 'show_address', 'show_prayers', 'show_events']


class MinistryPreferencesForm(forms.ModelForm):
    """Form for updating ministry preferences"""

    class Meta:
        model = MinistryPreferences
        fields = [
            'worship_team', 'children_ministry', 'youth_ministry',
            'outreach_ministry', 'prayer_team', 'hospitality_team',
            'sunday_morning', 'sunday_evening', 'weekdays', 'special_events',
            'spiritual_gifts'
        ]
        widgets = {
            'spiritual_gifts': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class ContentSettingsForm(forms.ModelForm):
    """Form for updating content settings"""

    class Meta:
        model = ContentSettings
        fields = [
            'show_sermons', 'show_devotionals', 'show_bible_studies',
            'show_community_posts', 'agree_guidelines'
        ]


class AdvancedSettingsForm(forms.Form):
    """Form for advanced settings"""
    data_export = forms.BooleanField(required=False)



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        exclude = ['user', 'slug', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'baptism_date': forms.DateInput(attrs={'type': 'date'}),
            'membership_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('profile_image', css_class='col-md-6'),
                Column('date_of_birth', css_class='col-md-6'),
            ),
            Row(
                Column('phone_number', css_class='col-md-6'),
                Column('marital_status', css_class='col-md-6'),
            ),
            'address',
            Row(
                Column('baptism_date', css_class='col-md-6'),
                Column('membership_date', css_class='col-md-6'),
            ),
            'membership_status',
            Row(
                Column('skills', css_class='col-md-6'),
                Column('ministries', css_class='col-md-6'),
            ),
            'bio',
            Row(
                Column('emergency_contact_name', css_class='col-md-6'),
                Column('emergency_contact_phone', css_class='col-md-6'),
            ),
            'is_public',
            Submit('submit', 'Save Profile', css_class='btn btn-primary mt-3')
        )



class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['password', 'new_password1', 'new_password2']


class UserProfileForm(forms.ModelForm):
    class Meta:

        model = UserProfile

        exclude = ['user', 'slug', 'channel']  # Fields to exclude

        widgets = {

            'birth_date': forms.DateInput(attrs={'type': 'date'}),

            'bio': forms.Textarea(attrs={'rows': 4}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'ministry': forms.Select(attrs={'class': 'form-select'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

"""
class ReportForm(forms.Form):
    class Meta:
        model = Report
        fields = ['user', 'content_type', 'content_id', 'content_object', 'reason', 'timestamp']


"""
class JoinCommunityForm(forms.Form):
    community_id = forms.IntegerField(widget=forms.HiddenInput())



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        exclude = ['slug', 'channel', 'google_picture', 'google_username']

# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'channel', 'google_picture', 'google_username']


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
