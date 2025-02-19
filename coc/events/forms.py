from .models import *
from django import forms
from django import forms
from .models import Event
from django.utils import timezone
from datetime import datetime

from django import forms
from .models import Event
from django.utils import timezone
from django import forms
from django.utils import timezone
from .models import Event
from django import forms
from django.utils import timezone

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'location',
            'start_date', 'start_time', 'end_date', 'end_time',
            'max_participants', 'is_published'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time')

        if all([start_date, start_time, end_date, end_time]):
            # Convert to datetime objects for comparison
            start_datetime = timezone.make_aware(
                datetime.combine(start_date, start_time)
            )
            end_datetime = timezone.make_aware(
                datetime.combine(end_date, end_time)
            )

            if end_datetime < start_datetime:
                raise forms.ValidationError('End date/time must be after start date/time')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make certain fields required
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['event_type'].required = True
        self.fields['start_date'].required = True
        self.fields['start_time'].required = True
        self.fields['end_time'].required = True

        # Add Bootstrap classes
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs['class'] = 'form-control'



class LiveStreamForm(forms.ModelForm):
    class Meta:
        model = LiveStream
        fields = ['title', 'description', 'scheduled_time', 'thumbnail']
        widgets = {
            'scheduled_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
