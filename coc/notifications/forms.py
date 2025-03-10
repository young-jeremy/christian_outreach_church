# notifications/forms.py
from .models import Notifications
from django import forms
from accounts.models import *
# notifications/forms.py
from django import forms
from .models import NotificationSettings
# notifications/forms.py
from django import forms
from .models import NotificationSettings


class NotificationsSettingsForm(forms.ModelForm):
    """Form for updating notification settings"""

    class Meta:
        model = NotificationSettings
        fields = [
            'email_notifications', 'password_change_notifications',
            'weekly_newsletter', 'sermon_notifications',
            'prayer_requests', 'ministry_updates', 'event_reminders',
            'volunteer_opportunities', 'bible_studies', 'devotionals'
        ]


class NotificationSettingsForm(forms.Form):
    email_notifications = forms.BooleanField(
        required=False,
        label="Receive email notifications",
        initial=True,
    )
    password_change_notifications = forms.BooleanField(
        required=False,
        label="Receive password change notifications",
        initial=True,
    )
    weekly_newsletter = forms.BooleanField(
        required=False,
        label="Subscribe to weekly newsletter",
        initial=True,
    )
    product_promotions = forms.BooleanField(
        required=False,
        label="Receive product promotion updates",
        initial=True,
    )



class MarkNotificationAsReadForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = ['is_read']

    def __init__(self, *args, **kwargs):
        super(MarkNotificationAsReadForm, self).__init__(*args, **kwargs)
        # Setting the initial value of is_read to True (for marking the notification as read)
        self.fields['is_read'].initial = True


