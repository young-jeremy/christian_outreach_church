from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.core.validators import FileExtensionValidator
from django_summernote.widgets import SummernoteWidget

from accounts.models import User
from .models import MensMinistry, MensEvent
from .models import SeniorsMinistry, SeniorsEvent, TransportationRequest
from .models import SinglesMinistry, SinglesEvent, MentorshipRequest, SinglesResource
from .models import WomensMinistry, MinistryEvent
# ... rest of your forms ...
from .models import WorshipService
from .models import YouthEventPayment, PermissionSlip, AttendanceRecord
from .models import YouthProgram


class WomensMinistryForm(forms.ModelForm):
    class Meta:
        model = WomensMinistry
        fields = ['title', 'description', 'ministry_type', 'meeting_time', 'location', 'image']
        widgets = {
            'meeting_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class MinistryEventForm(forms.ModelForm):
    class Meta:
        model = MinistryEvent
        fields = ['title', 'description', 'date', 'location', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }



class WorshipServiceForm(forms.ModelForm):
    class Meta:
        model = WorshipService
        fields = [
            'title', 'service_type', 'status', 'date', 'theme',
            'description', 'location', 'is_online', 'live_stream_url',
            'meeting_link', 'worship_leader', 'preacher', 'team_members',
            'song_list', 'service_order', 'notes', 'special_notes',
            'image', 'banner', 'registration_required', 'max_attendees',
            'registration_deadline', 'is_featured', 'is_special_event'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'registration_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={'rows': 4}),
            'song_list': forms.Textarea(attrs={'rows': 4}),
            'service_order': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'special_notes': forms.Textarea(attrs={'rows': 4}),
            'team_members': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


from .models import (
    # Core models
    EventRegistration, EventFeedback,  # Bible Study related
    BibleStudy, SermonCategory, SermonSeries, Sermon,
    SermonComment, SermonNote, SermonTag,
    
    # Service related
    SongRequest,
    
    # Youth and Children
    YouthEvent, YouthMinistry, ChildrenProgram,
    ChildrensMinistry, Child,
    
    # Groups and Registration
    SmallGroup, MinistryRegistration,
    
    # Couples Ministry
    CoupleEvent, CounselingSession,
    CoupleResource, CoupleJournal, DateNightIdea,
    CouplePrayerRequest,
    
    # Prayer and Notifications
    PrayerRequest, PrayerUpdate, NotificationPreferences,
    
    # Forums and Topics
    Topic, Post, ForumCategory,
    
    # Family Ministry
    FamilyGroup, FamilyEvent, ParentingResource,
    FamilyCounseling, FamilyDiscussion, DiscussionComment,
    
    # New Believers
    NewBelieverProfile, DiscipleshipTrack, DiscipleshipModule,
    MentorshipSession, PrayerJournal, BibleReadingPlan,

    # Marriage Ministry
    MarriageMinistry, MarriageEnrollment, MarriageResource,
    MarriageCounseling, MarriageEvent,
    
    # Volunteer
    VolunteerOpportunity, VolunteerSignup,
    
    # Video Related
    WatchedVideo, DownloadedVideo, Category,
    Testimony
)

# Video related models
from videos.models import (
    ShortVideo, Comments,
    Playlist, PlaylistVideo, Queue, QueueItem
)
from django import forms
from django.utils import timezone
from datetime import datetime

from .models import Event  # Ensure you import your Event model

from django import forms
from .models import CounselingRequest

from django import forms
from .models import CounselingRequest


class CounselingRequestForm(forms.ModelForm):
    preferred_days = forms.MultipleChoiceField(
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CounselingRequest
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'preferred_contact',
            'counseling_category',
            'other_category',
            'reason_for_counseling',
            'preferred_days',
            'preferred_time',
            'urgency',
            'previous_counseling',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'preferred_contact': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'counseling_category': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'other_category': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Please specify if you selected Other'
            }),
            'reason_for_counseling': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded h-32',
                'rows': 4
            }),
            'preferred_time': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'urgency': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'previous_counseling': forms.CheckboxInput(attrs={'class': 'mr-2'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, phone))

        if len(phone) < 10:
            raise forms.ValidationError("Please enter a valid phone number")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('counseling_category')
        other_category = cleaned_data.get('other_category')

        if category == 'other' and not other_category:
            raise forms.ValidationError({
                'other_category': "Please specify the counseling category"
            })
        return cleaned_data

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'category', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': SummernoteWidget(),
        }


class VolunteerOpportunityForm(forms.ModelForm):
    class Meta:
        model = VolunteerOpportunity
        exclude = ['slug', 'volunteers', 'created_at', 'updated_at']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-8'),
                Column('ministry', css_class='col-md-4'),
            ),
            'description',
            Row(
                Column('coordinator', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            'requirements',
            Row(
                Column('frequency', css_class='col-md-6'),
                Column('time_commitment', css_class='col-md-6'),
            ),
            'location',
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            'max_volunteers',
            Submit('submit', 'Save Opportunity', css_class='btn btn-primary mt-3')
        )


class VolunteerSignupForm(forms.ModelForm):
    class Meta:
        model = VolunteerSignup
        fields = ['notes', 'availability']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'availability': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'notes',
            'availability',
            Submit('submit', 'Sign Up', css_class='btn btn-primary mt-3')
        )




class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'image',
            'start_date', 'start_time', 'end_date', 'end_time',
            'is_online', 'online_link', 'location',
            'registration_required', 'is_published', 'max_participants',
            'is_recurring', 'registration_deadline', 'speakers'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the event'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_online': forms.CheckboxInput(attrs={'class': 'form-check-input', 'onchange': 'toggleLocationFields(this)'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event location'}),
            'online_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter meeting link'}),
            'registration_required': forms.CheckboxInput(attrs={'class': 'form-check-input', 'onchange': 'toggleRegistrationFields(this)'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        registration_deadline = cleaned_data.get('registration_deadline')

        # Ensure valid start date
        if start_date:
            today = timezone.now().date()
            if start_date < today:
                raise forms.ValidationError("Event cannot start in the past")

        # Ensure end date is after start date
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date")

        # Ensure end time is after start time
        if start_time and end_time:
            if start_date == end_date and end_time <= start_time:
                raise forms.ValidationError("End time must be after start time")

        # Ensure registration deadline is before event start
        if registration_deadline and start_date and start_time:
            event_start = datetime.combine(start_date, start_time)

            # Convert to timezone-aware if necessary
            if timezone.is_naive(event_start):
                event_start = timezone.make_aware(event_start)

            if timezone.is_naive(registration_deadline):
                registration_deadline = timezone.make_aware(registration_deadline)

            if registration_deadline >= event_start:
                raise forms.ValidationError("Registration deadline must be before event start")

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        registration_deadline = cleaned_data.get('registration_deadline')

        # Ensure start_date is compared correctly
        if start_date and timezone.now().date() != start_date:  # Convert timezone.now() to date()
            raise forms.ValidationError("Event cannot start in the past")

        # Ensure end_date is compared correctly
        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date")

        # Ensure time comparison is valid
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time")

        # Ensure registration_deadline is before event start
        if registration_deadline and start_date and start_time:
            # Convert start_date & start_time to datetime
            event_start = timezone.make_aware(datetime.combine(start_date, start_time))

            if registration_deadline >= event_start:
                raise forms.ValidationError("Registration deadline must be before event start time")

        return cleaned_data



class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3})
        }


class NotificationPreferencesForm(forms.ModelForm):
    class Meta:
        model = NotificationPreferences
        fields = [
            'email_updates', 'email_new_warriors',
            'sms_updates', 'sms_new_warriors',
            'real_time_notifications', 'phone_number'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+1234567890'
            })
        }


class PrayerStatusForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }


class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = ['title', 'content', 'prayer_request', ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class PrayerUpdateForm(forms.ModelForm):
    class Meta:
        model = PrayerUpdate
        fields = ['update_text']
        widgets = {
            'update_text': forms.Textarea(attrs={'rows': 3})
        }


class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        exclude = ['couple', 'created_at', 'is_answered', 'answer_testimony']
        widgets = {
            'request': forms.Textarea(attrs={'rows': 4}),
        }


class SmallGroupForm(forms.ModelForm):
    leaders = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        help_text='Select additional leaders for this group'
    )

    class Meta:
        model = SmallGroup
        fields = [
            'name', 'description', 'group_type', 'image',
            'max_members', 'meeting_frequency', 'meeting_day',
            'meeting_time', 'is_online', 'location',
            'is_accepting_members', 'requires_approval', 'leaders'
        ]
        widgets = {
            'meeting_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'Physical location or online meeting link'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter group name'})
        self.fields['max_members'].widget.attrs.update({'min': '2', 'max': '50'})

        # Update queryset to exclude superusers and staff
        self.fields['leaders'].queryset = User.objects.filter(
            is_active=True,
            is_admin=False
        ).order_by('username')


class SmallGroupJoinForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text='Why would you like to join this group?'
    )


class YouthEventForm(forms.ModelForm):
    class Meta:
        model = YouthEvent
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'schedule': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ChildrenProgramForm(forms.ModelForm):
    class Meta:
        model = ChildrenProgram
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'curriculum': forms.Textarea(attrs={'rows': 4}),
            'materials_needed': forms.Textarea(attrs={'rows': 3}),
            'parent_instructions': forms.Textarea(attrs={'rows': 3})
        }


class SongRequestForm(forms.ModelForm):
    class Meta:
        model = SongRequest
        fields = [
            'song_title',
            'artist',
            'preferred_date',
            'occasion',
            'reason',
            'notes',
            'is_urgent'
        ]
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class BibleStudyForm(forms.ModelForm):
    class Meta:
        model = BibleStudy
        exclude = ['teacher', 'participants', 'created_at', 'updated_at']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'study_outline': forms.Textarea(attrs={'rows': 4}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }



class YouthMinistryForm(forms.ModelForm):
    class Meta:
        model = YouthMinistry
        fields = [
            'title', 'event_type', 'description', 'date', 'location',
            'age_range', 'coordinator', 'max_participants', 'image',
            'registration_deadline'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ChildrensProgramForm(forms.ModelForm):
    class Meta:
        model = ChildrensMinistry
        fields = [
            'title', 'description', 'age_group', 'program_type',
            'meeting_time', 'location', 'image', 'max_capacity',
            'curriculum', 'safety_guidelines', 'allergies_aware'
        ]
        widgets = {
            'meeting_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'safety_guidelines': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }

class ChildRegistrationForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = [
            'first_name', 'last_name', 'date_of_birth',
            'allergies', 'medical_notes', 'emergency_contact',
            'photo_permission', 'special_needs', 'pickup_allowed_by'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'allergies': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control'}
            ),
            'medical_notes': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control'}
            ),
        }


class MinistryRegistrationForm(forms.ModelForm):
    class Meta:
        model = MinistryRegistration
        fields = ['role', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4})
        }


class SermonSeriesForm(forms.ModelForm):
    class Meta:
        model = SermonSeries
        fields = ['title', 'description', 'thumbnail', 'start_date', 'end_date', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        exclude = ['slug', 'views', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date_preached': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.TimeInput(attrs={'type': 'time', 'step': '1'})
        }


class SermonCommentForm(forms.ModelForm):
    class Meta:
        model = SermonComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }

class SermonNoteForm(forms.ModelForm):
    # Convert the JSONField to a more user-friendly textarea
    main_points = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Enter each main point on a new line'
        }),
        help_text="Enter each point on a new line. They will be automatically formatted."
    )

    class Meta:
        model = SermonNote
        fields = [
            'title',
            'preacher',
            'date',
            'scripture_reference',
            'category',
            'introduction',
            'main_points',
            'conclusion',
            'key_verses',
            'practical_applications',
            'additional_notes',
            'audio_recording',
            'presentation_file',
            'tags',
            'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sermon title'
            }),
            'preacher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter preacher name'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'scripture_reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., John 3:16-17'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'introduction': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter sermon introduction'
            }),
            'conclusion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter sermon conclusion'
            }),
            'key_verses': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter key Bible verses'
            }),
            'practical_applications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter practical applications'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter any additional notes'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_main_points(self):
        """Convert the textarea input into a list for the JSONField"""
        points = self.cleaned_data['main_points']
        # Split by newlines and remove empty lines
        points_list = [p.strip() for p in points.split('\n') if p.strip()]
        return points_list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're editing an existing sermon note, convert the JSON list back to newline-separated text
        if self.instance.pk and isinstance(self.instance.main_points, list):
            self.initial['main_points'] = '\n'.join(self.instance.main_points)


class SermonTagForm(forms.ModelForm):
    class Meta:
        model = SermonTag
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = SermonCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ShortVideoForm(forms.ModelForm):
    class Meta:
        model = ShortVideo
        fields = [
            'title', 'description', 'video_file', 'thumbnail',
            'duration', 'category', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'duration': forms.TimeInput(attrs={'type': 'time', 'step': '1'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'form-control'
            }),
        }


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description', 'thumbnail', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class PlaylistVideoForm(forms.ModelForm):
    class Meta:
        model = PlaylistVideo
        fields = ['position']


class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['videos']
        widgets = {
            'videos': forms.SelectMultiple(attrs={'class': 'select2'}),
        }


class QueueItemForm(forms.ModelForm):
    class Meta:
        model = QueueItem
        fields = ['position']


class WatchedVideoForm(forms.ModelForm):
    class Meta:
        model = WatchedVideo
        fields = ['watch_duration', 'completed']
        widgets = {
            'watch_duration': forms.TimeInput(attrs={'type': 'time', 'step': '1'}),
        }


class DownloadedVideoForm(forms.ModelForm):
    class Meta:
        model = DownloadedVideo
        fields = ['video']


# Form for handling file uploads with validation
class VideoUploadForm(forms.Form):
    video_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm'])]
    )
    thumbnail = forms.ImageField()


# Form for handling search
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('-views', 'Most Viewed'),
            ('-likes', 'Most Liked'),
        ],
        required=False
    )


# Form for bulk actions
class BulkActionForm(forms.Form):
    ACTIONS = [
        ('delete', 'Delete Selected'),
        ('download', 'Download Selected'),
        ('add_to_playlist', 'Add to Playlist'),
    ]

    action = forms.ChoiceField(choices=ACTIONS)
    items = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    playlist = forms.ModelChoiceField(
        queryset=Playlist.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['playlist'].queryset = Playlist.objects.filter(creator=user)


class TopicSearchForm(forms.Form):
    query = forms.CharField(required=False)
    category = forms.ModelChoiceField(
        queryset=ForumCategory.objects.all(),
        required=False,
        empty_label="All Categories"
    )


class MarriageMinistryForm(forms.ModelForm):
    class Meta:
        model = MarriageMinistry
        exclude = ['slug', 'created_at', 'updated_at']
        widgets = {
            'description': SummernoteWidget(),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time'}),
        }


from django import forms
from .models import CoupleProfile

class CoupleProfileForm(forms.ModelForm):
    class Meta:
        model = CoupleProfile
        fields = [
            'partner_name', 'partner_email', 'partner_phone',
            'anniversary', 'marriage_stage', 'profile_image',
            'about_us', 'interests', 'preferred_contact_method',
            'is_public', 'show_anniversary'
        ]
        exclude = ['user']  # Explicitly exclude the user field
        widgets = {
            'anniversary': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'about_us': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'interests': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'marriage_stage': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'preferred_contact_method': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

    def clean_partner_phone(self):
        phone = self.cleaned_data.get('partner_phone')
        if phone:
            # Remove any spaces or special characters except '+'
            phone = ''.join(c for c in phone if c.isdigit() or c == '+')
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required that shouldn't be null
        self.fields['partner_name'].required = True
        self.fields['partner_email'].required = True
        self.fields['marriage_stage'].required = True
        self.fields['preferred_contact_method'].required = True


class MarriageEnrollmentForm(forms.ModelForm):
    class Meta:
        model = MarriageEnrollment
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MarriageResourceForm(forms.ModelForm):
    class Meta:
        model = MarriageResource
        exclude = ['created_at', 'updated_at']
        widgets = {
            'content': SummernoteWidget(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class MarriageCounselingForm(forms.ModelForm):
    class Meta:
        model = MarriageCounseling
        exclude = ['created_at', 'status']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MarriageEventForm(forms.ModelForm):
    class Meta:
        model = MarriageEvent
        exclude = ['created_at']
        widgets = {
            'description': SummernoteWidget(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'registration_deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class FamilyGroupForm(forms.ModelForm):
    class Meta:
        model = FamilyGroup
        fields = ['name', 'description', 'members']
        widgets = {
            'description': SummernoteWidget(),
        }


class FamilyEventForm(forms.ModelForm):
    class Meta:
        model = FamilyEvent
        exclude = ['organizer', 'participants', 'created_at', 'slug']
        widgets = {
            'description': SummernoteWidget(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ParentingResourceForm(forms.ModelForm):
    class Meta:
        model = ParentingResource
        exclude = ['created_by', 'created_at', 'updated_at', 'slug']
        widgets = {
            'content': SummernoteWidget(),
        }


class FamilyCounselingForm(forms.ModelForm):
    class Meta:
        model = FamilyCounseling
        exclude = ['family', 'created_at', 'status']
        widgets = {
            'scheduled_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class FamilyDiscussionForm(forms.ModelForm):
    class Meta:
        model = FamilyDiscussion
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }


class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...'})
        }


class NewBelieverProfileForm(forms.ModelForm):
    class Meta:
        model = NewBelieverProfile
        exclude = ['user', ]
        widgets = {
            'salvation_date': forms.DateInput(attrs={'type': 'date'}),
            'baptism_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DiscipleshipTrackForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipTrack
        exclude = ['created_at', 'slug']
        widgets = {
            'description': SummernoteWidget(),
        }


class DiscipleshipModuleForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipModule
        fields = '__all__'
        widgets = {
            'content': SummernoteWidget(),
        }


class MentorshipSessionForm(forms.ModelForm):
    class Meta:
        model = MentorshipSession
        exclude = ['completed']
        widgets = {
            'scheduled_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class PrayerJournalForm(forms.ModelForm):
    class Meta:
        model = PrayerJournal
        exclude = ['believer', 'created_at', 'updated_at']
        widgets = {
            'answer_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BibleReadingPlanForm(forms.ModelForm):

    class Meta:
        model = BibleReadingPlan
        fields = ['title', 'description', 'plan_type', 'start_date', 'end_date', 'total_chapters']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CoupleEventForm(forms.ModelForm):
    class Meta:
        model = CoupleEvent
        exclude = ['created_at', 'slug']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': SummernoteWidget()
        }


class CounselingSessionForm(forms.ModelForm):
    class Meta:
        model = CounselingSession
        exclude = ['completed', 'private_notes']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'homework_assigned': forms.Textarea(attrs={'rows': 4})
        }


class CoupleResourceForm(forms.ModelForm):
    class Meta:
        model = CoupleResource
        exclude = ['created_at', 'download_count']
        widgets = {
            'description': SummernoteWidget(),
            'content': SummernoteWidget()
        }


class CoupleJournalForm(forms.ModelForm):
    class Meta:
        model = CoupleJournal
        exclude = ['couple', 'created_at']
        widgets = {
            'content': SummernoteWidget(),
            'mood_rating': forms.RadioSelect(),
        }


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = CoupleJournal
        fields = ['title', 'content', 'mood_rating', 'shared_with_counselor', 'tags']
        widgets = {
            'content': SummernoteWidget(),
            'mood_rating': forms.RadioSelect()
        }


class CouplePrayerRequestForm(forms.ModelForm):
    class Meta:
        model = CouplePrayerRequest
        fields = ['title', 'request', 'is_private']
        widgets = {
            'request': forms.Textarea(attrs={'rows': 4})
        }


class EventFeedbackForm(forms.ModelForm):
    class Meta:
        model = EventFeedback
        fields = ['rating', 'comment', 'anonymous']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4})
        }


class SermonCategoryForm(forms.ModelForm):
    class Meta:
        model = SermonCategory
        fields = ['name', 'description', 'icon', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


class DateNightIdeaForm(forms.ModelForm):
    class Meta:
        model = DateNightIdea
        fields = ['title', 'description', 'estimated_cost', 'duration', 'location_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'duration': forms.TimeInput(attrs={'type': 'time'})
        }



class MensMinistryForm(forms.ModelForm):
    class Meta:
        model = MensMinistry
        fields = ['title', 'description', 'ministry_type', 'meeting_time',
                 'location', 'image', 'vision', 'mission']
        widgets = {
            'meeting_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'vision': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'mission': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }

class MensEventForm(forms.ModelForm):
    class Meta:
        model = MensEvent
        fields = ['title', 'description', 'date', 'location', 'image',
                 'event_type', 'max_attendees', 'registration_deadline']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'registration_deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
        }

# Add to your existing forms.py
class YouthProgramForm(forms.ModelForm):
    class Meta:
        model = YouthProgram
        fields = [
            'title', 'description', 'program_type', 'age_group',
            'meeting_time', 'location', 'image', 'max_participants',
            'requirements', 'parent_consent_required'
        ]
        widgets = {
            'meeting_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'requirements': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = YouthEventPayment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(choices=[
                ('CARD', 'Credit/Debit Card'),
                ('MPESA', 'M-PESA'),
                ('CASH', 'Cash')
            ])
        }

class PermissionSlipForm(forms.ModelForm):
    class Meta:
        model = PermissionSlip
        fields = ['document']
        widgets = {
            'document': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
        }

    def clean_document(self):
        document = self.cleaned_data.get('document')
        if document:
            if document.size > 5*1024*1024:  # 5MB limit
                raise forms.ValidationError("File size must be under 5MB")
            ext = document.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError("Only PDF and Word documents are allowed")
        return document

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['notes']




class SeniorsMinistryForm(forms.ModelForm):
    class Meta:
        model = SeniorsMinistry
        fields = [
            'title', 'description', 'activity_type', 'meeting_time',
            'location', 'image', 'max_participants', 'transportation_provided',
            'accessibility_notes', 'health_guidelines'
        ]
        widgets = {
            'meeting_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'accessibility_notes': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'health_guidelines': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }

class TransportationRequestForm(forms.ModelForm):
    class Meta:
        model = TransportationRequest
        fields = [
            'pickup_address', 'special_needs', 'emergency_contact',
            'preferred_pickup_time', 'notes'
        ]
        widgets = {
            'preferred_pickup_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'notes': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }

class SeniorsEventForm(forms.ModelForm):
    class Meta:
        model = SeniorsEvent
        fields = [
            'title', 'description', 'date', 'location',
            'max_participants', 'transportation_provided',
            'registration_deadline', 'image', 'ministry'
        ]
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'registration_deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
        }


class SinglesMinistryForm(forms.ModelForm):
    class Meta:
        model = SinglesMinistry
        fields = [
            'title', 'description', 'activity_type', 'meeting_time',
            'location', 'image', 'max_participants', 'age_group',
            'relationship_status', 'guidelines'
        ]
        widgets = {
            'meeting_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'guidelines': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'age_group': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'relationship_status': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'activity_type': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

class SinglesEventForm(forms.ModelForm):
    class Meta:
        model = SinglesEvent
        fields = [
            'ministry', 'title', 'description', 'date',
            'location', 'image', 'max_participants',
            'registration_deadline', 'is_couples_allowed',
            'event_cost', 'dress_code', 'special_instructions'
        ]
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'registration_deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'special_instructions': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'ministry': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'event_cost': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        registration_deadline = cleaned_data.get('registration_deadline')

        if date and registration_deadline and registration_deadline > date:
            raise forms.ValidationError(
                "Registration deadline cannot be after the event date."
            )
        return cleaned_data

class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = [
            'areas_of_focus', 'preferred_meeting_times', 'notes'
        ]
        widgets = {
            'areas_of_focus': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-control',
                    'placeholder': 'What areas would you like mentorship in?'
                }
            ),
            'preferred_meeting_times': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g., Weekday evenings, Saturday mornings'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'Any additional information you\'d like to share'
                }
            ),
        }

class SinglesResourceForm(forms.ModelForm):
    class Meta:
        model = SinglesResource
        fields = [
            'title', 'category', 'content', 'document', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'category': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'content': forms.Textarea(
                attrs={
                    'rows': 6,
                    'class': 'form-control',
                    'id': 'resource-content'
                }
            ),
        }

class MentorshipMatchForm(forms.Form):
    mentor = forms.ModelChoiceField(
        queryset=None,  # Set in __init__
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a mentor"
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Add any notes about this match'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        potential_mentors = kwargs.pop('potential_mentors', None)
        super().__init__(*args, **kwargs)
        if potential_mentors is not None:
            self.fields['mentor'].queryset = potential_mentors

class SinglesEventRegistrationForm(forms.Form):
    special_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Any special requirements or dietary restrictions?'
            }
        )
    )
    emergency_contact = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact name and phone number'
            }
        )
    )
    accept_guidelines = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        ),
        help_text='I have read and accept the event guidelines'
    )