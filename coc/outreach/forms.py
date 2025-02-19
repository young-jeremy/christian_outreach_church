from django import forms
from .models import *


class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['subject', 'request', 'is_anonymous']
        widgets = {
            'request': forms.Textarea(attrs={'rows': 4}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class DevotionalForm(forms.ModelForm):
    class Meta:
        model = Devotional
        fields = ['title', 'content', 'scripture']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }


class SmallGroupForm(forms.ModelForm):
    class Meta:
        model = SmallGroup
        fields = ['name', 'description', 'meeting_time', 'location']
