from django import forms

from ..models.bible_college import (
    BibleCollegeProgram, BibleCollegeCourse, BibleCollegeStudent,
    BibleCollegeCourseEnrollment, BibleCollegeAssignment,
    BibleCollegeAssignmentSubmission
)


class BibleCollegeStudentForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeStudent
        fields = ['program', 'testimony', 'spiritual_reference']
        widgets = {
            'testimony': forms.Textarea(attrs={'rows': 4}),
        }


class BibleCollegeAssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeAssignmentSubmission
        fields = ['submitted_file']


class BibleCollegeCourseEnrollmentForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(
        queryset=BibleCollegeCourse.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)
        if program:
            self.fields['courses'].queryset = BibleCollegeCourse.objects.filter(program=program)


class BibleCollegeGradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeAssignmentSubmission
        fields = ['marks_obtained', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }
