from .models import *
from django import forms

from .models import *
from .models import (DiscipleshipTrack, DiscipleshipModule, DiscipleshipLesson,
                     MentorshipRelationship, DiscipleshipProgress, MentorshipMeeting)
from .models import (HospitalVolunteer, VisitSchedule, PatientRequest,
                     HospitalVisitReport)
from .models import (VolunteerApplication, PrisonVisit, PrisonVisitReport,
                     MinistryResource)


class HospitalVolunteerForm(forms.ModelForm):
    class Meta:
        model = HospitalVolunteer
        fields = ['hospitals', 'services', 'availability', 'emergency_contact',
                  'emergency_phone', 'medical_training']
        widgets = {
            'hospitals': forms.CheckboxSelectMultiple(),
            'services': forms.CheckboxSelectMultiple(),
            'availability': forms.Textarea(attrs={'rows': 4}),
            'medical_training': forms.Textarea(attrs={'rows': 4}),
        }


class VisitScheduleForm(forms.ModelForm):
    class Meta:
        model = VisitSchedule
        fields = ['hospital', 'department', 'service', 'date', 'volunteers', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'volunteers': forms.CheckboxSelectMultiple(),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class PatientRequestForm(forms.ModelForm):
    class Meta:
        model = PatientRequest
        fields = ['patient_name', 'room_number', 'department', 'service_requested',
                  'priority', 'special_notes', 'preferred_time']
        widgets = {
            'preferred_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'special_notes': forms.Textarea(attrs={'rows': 4}),
        }


class PrisonVisitReportForm(forms.ModelForm):
    class Meta:
        model = PrisonVisitReport
        fields = ['inmates_attended', 'activities_conducted', 'prayer_requests',
                  'testimonies', 'challenges', 'follow_up_needed', 'resources_used']
        widgets = {
            'activities_conducted': forms.Textarea(attrs={'rows': 4}),
            'prayer_requests': forms.Textarea(attrs={'rows': 4}),
            'testimonies': forms.Textarea(attrs={'rows': 4}),
            'challenges': forms.Textarea(attrs={'rows': 4}),
            'follow_up_needed': forms.Textarea(attrs={'rows': 4}),
            'resources_used': forms.Textarea(attrs={'rows': 4}),
        }


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['facility', 'programs', 'experience', 'motivation',
                  'availability', 'references', 'background_check_consent']
        widgets = {
            'programs': forms.CheckboxSelectMultiple(),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'motivation': forms.Textarea(attrs={'rows': 4}),
            'availability': forms.Textarea(attrs={'rows': 4}),
            'references': forms.Textarea(attrs={'rows': 4}),
        }


class PrisonVisitForm(forms.ModelForm):
    class Meta:
        model = PrisonVisit
        fields = ['facility', 'program', 'date', 'volunteers', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'volunteers': forms.CheckboxSelectMultiple(),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class HospitalVisitReportForm(forms.ModelForm):
    class Meta:
        model = HospitalVisitReport
        fields = ['patients_visited', 'prayer_requests', 'testimonies',
                  'challenges', 'follow_up_needed']
        widgets = {
            'prayer_requests': forms.Textarea(attrs={'rows': 4}),
            'testimonies': forms.Textarea(attrs={'rows': 4}),
            'challenges': forms.Textarea(attrs={'rows': 4}),
            'follow_up_needed': forms.Textarea(attrs={'rows': 4}),
        }


class ResourceRequestForm(forms.ModelForm):
    class Meta:
        model = MinistryResource
        fields = ['title', 'resource_type', 'description', 'quantity',
                  'facility', 'program', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class DiscipleshipTrackForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipTrack
        fields = ['title', 'description', 'level', 'duration_weeks',
                  'prerequisites', 'featured_image']


class DiscipleshipModuleForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipModule
        fields = ['title', 'description', 'order', 'learning_objectives',
                  'estimated_hours']


class DiscipleshipLessonForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipLesson
        fields = ['title', 'content', 'scripture_references',
                  'reflection_questions', 'order', 'video_url',
                  'additional_resources']


class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRelationship
        fields = ['track', 'goals', 'meeting_frequency']
        widgets = {
            'goals': forms.Textarea(attrs={'rows': 4}),
        }


class LessonReflectionForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipProgress
        fields = ['reflection']
        widgets = {
            'reflection': forms.Textarea(attrs={'rows': 6}),
        }


class MentorshipMeetingForm(forms.ModelForm):
    class Meta:
        model = MentorshipMeeting
        fields = ['date', 'topics_discussed', 'action_items',
                  'next_meeting_date', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_meeting_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CharityCampaignForm(forms.ModelForm):
    class Meta:
        model = CharityCampaign
        fields = ['title', 'description', 'cause', 'target_amount', 'start_date',
                  'end_date', 'featured_image', 'beneficiary', 'contact_person',
                  'contact_email']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'message', 'anonymous']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1', 'step': '0.01'}),
        }


class CharityEventForm(forms.ModelForm):
    class Meta:
        model = CharityEvent
        fields = ['title', 'description', 'date', 'location', 'max_participants']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ServiceProjectForm(forms.ModelForm):
    class Meta:
        model = ServiceProject
        fields = ['title', 'category', 'description', 'location', 'organization',
                  'contact_person', 'contact_email', 'start_date', 'end_date',
                  'volunteers_needed', 'skills_required', 'featured_image']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ServiceHoursForm(forms.ModelForm):
    class Meta:
        model = ServiceHours
        fields = ['project', 'date', 'hours', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ServiceReflectionForm(forms.ModelForm):
    class Meta:
        model = ServiceReflection
        fields = ['reflection', 'impact', 'learning', 'images']



class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = [
            'title', 'description', 'location', 'start_date', 'end_date',
            'status', 'featured_image', 'budget', 'team_size', 'impact_summary'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mission title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the mission and its objectives'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mission location'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter budget amount'
            }),
            'team_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter team size'
            }),
            'impact_summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the expected or achieved impact'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date")
        return cleaned_data


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'category', 'description', 'mission', 'status',
            'start_date', 'end_date', 'location', 'project_lead',
            'contact_email', 'budget', 'featured_image', 'goals', 'outcomes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the project and its objectives'
            }),
            'mission': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project location'
            }),
            'project_lead': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project leader name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact email'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter budget amount'
            }),
            'goals': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List the project goals'
            }),
            'outcomes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe expected or achieved outcomes'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        mission = cleaned_data.get('mission')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date")

        if mission and start_date:
            if start_date < mission.start_date:
                raise forms.ValidationError("Project cannot start before its mission")
            if mission.end_date and end_date and end_date > mission.end_date:
                raise forms.ValidationError("Project cannot end after its mission")

        return cleaned_data


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter update title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the project update'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }