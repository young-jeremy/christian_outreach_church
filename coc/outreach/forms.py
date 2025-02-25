from django import forms
from .models import Mission, Project, ProjectUpdate


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