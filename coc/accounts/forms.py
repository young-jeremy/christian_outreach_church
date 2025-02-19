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


"""
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'"""

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
