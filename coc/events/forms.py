from datetime import datetime

from django import forms
from django.forms.widgets import FileInput
from django.utils import timezone

from .models import ArchivedVideo, VideoCategory
from .models import AudioMessage
from .models import Event
from .models import LiveStream, StreamChat
from .models import (
    NewsArticle, Newsletter,
    Announcement, TestimonialVideo
)
from .models import PhotoAlbum, Photo


class TestimonialVideoForm(forms.ModelForm):
    class Meta:
        model = TestimonialVideo
        fields = ['title', 'person_name', 'description', 'video_file', 'thumbnail', 'recorded_date']
        widgets = {
            'recorded_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AudioMessageForm(forms.ModelForm):
    class Meta:
        model = AudioMessage
        fields = ['title', 'description', 'audio_file', 'category', 'recorded_date']
        widgets = {
            'recorded_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MultipleFileInput(FileInput):
    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content', 'image', 'tags', 'is_published', 'featured']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'class': 'rich-text-editor'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'issue_number', 'publication_date',
                  'pdf_file', 'cover_image', 'description', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority', 'start_date',
                  'end_date', 'is_active', 'image', 'link']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TestimonialVideoForm(forms.ModelForm):
    class Meta:
        model = TestimonialVideo
        fields = ['title', 'person_name', 'video_file', 'thumbnail',
                  'description', 'recorded_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'recorded_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PhotoAlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['title', 'description', 'cover_image', 'is_public', 'event_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'is_featured']


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = ArchivedVideo
        fields = ['title', 'description', 'category', 'video_file', 'thumbnail', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class VideoCategoryForm(forms.ModelForm):
    class Meta:
        model = VideoCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class LiveStreamForm(forms.ModelForm):
    class Meta:
        model = LiveStream
        fields = ['title', 'description', 'scheduled_time', 'thumbnail']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class StreamChatForm(forms.ModelForm):
    class Meta:
        model = StreamChat
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message...'
            })
        }

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


