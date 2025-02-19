from django import forms
from .models import Opportunity, Volunteer

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'requirements', 'location', 'date', 'duration', 'slots']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }

class VolunteerSignupForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any additional information or special requirements...'}),
        } 