from django import forms

from .models import (
    BibleCollegeProgram, BibleCollegeCourse, BibleCollegeStudent,
    BibleCollegeEnrollment, BibleCollegeAssignment, BibleCollegeSubmission,
    BibleCollegeFaculty
)
from .models import (BiblicalCourse, CourseModule, Lesson, Assignment,
                     StudentEnrollment, AssignmentSubmission, Discussion,
                     DiscussionReply)
from .models import (
    ChristianEducationLevel, ChristianCourse, ChristianModule,
    ChristianAssignment, ChristianAssignmentSubmission,
    ChristianDiscussion, ChristianDiscussionPost,
    ChristianEnrollment
)
from .models import (
    ChristianMentorshipSession,
    ChristianMentorshipApplication,
    ChristianMentorshipFeedback
)
from .models import (
    LeadershipTraining, TrainingModule, TrainingSession,
    LeadershipAssessment, ParticipantEnrollment, AssessmentSubmission,
    MentorshipSession
)
from .models import SundaySchoolMaterial, Activity, TeachingResource, Feedback
from .models import TheologicalResource, StudyNote, ResourceReview, Bibliography


class BibleCollegeProgramForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeProgram
        fields = ['name', 'level', 'description', 'duration_years', 'credits_required']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class BibleCollegeCourseForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeCourse
        fields = [
            'program', 'code', 'title', 'description',
            'credits', 'semester', 'year_level',
            'prerequisites', 'syllabus'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prerequisites': forms.SelectMultiple(attrs={'class': 'select2'}),
        }


class BibleCollegeStudentForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeStudent
        fields = ['program', 'testimony', 'spiritual_reference']
        widgets = {
            'testimony': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your testimony and why you want to study at our Bible College...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spiritual_reference'].help_text = (
            'Please upload a reference letter from your pastor or spiritual mentor'
        )


class BibleCollegeEnrollmentForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeEnrollment
        fields = ['course', 'semester', 'year']


class BibleCollegeAssignmentForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeAssignment
        fields = ['title', 'description', 'due_date', 'total_marks', 'weight_percentage']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class BibleCollegeSubmissionForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeSubmission
        fields = ['submitted_file']
        widgets = {
            'submitted_file': forms.FileInput(attrs={'class': 'form-control'})
        }


class BibleCollegeFacultyForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeFaculty
        fields = ['title', 'qualifications', 'bio', 'office_hours', 'courses', 'profile_image']
        widgets = {
            'qualifications': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'office_hours': forms.Textarea(attrs={'rows': 2}),
            'courses': forms.SelectMultiple(attrs={'class': 'select2'})
        }


class BibleCollegeGradeForm(forms.ModelForm):
    class Meta:
        model = BibleCollegeSubmission
        fields = ['marks_obtained', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }


class ChristianMentorshipSessionForm(forms.ModelForm):
    class Meta:
        model = ChristianMentorshipSession
        fields = [
            'topic', 'scripture_focus', 'description',
            'date', 'start_time', 'end_time',
            'max_participants', 'study_materials'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'})
        }


class ChristianMentorshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ChristianMentorshipApplication
        fields = ['spiritual_goals', 'faith_background', 'ministry_involvement', 'commitment_hours']
        widgets = {
            'spiritual_goals': forms.Textarea(attrs={'rows': 4}),
            'faith_background': forms.Textarea(attrs={'rows': 4}),
            'ministry_involvement': forms.Textarea(attrs={'rows': 4})
        }


class ChristianMentorshipFeedbackForm(forms.ModelForm):
    class Meta:
        model = ChristianMentorshipFeedback
        fields = ['spiritual_growth_rating', 'mentorship_quality', 'feedback', 'prayer_requests']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
            'prayer_requests': forms.Textarea(attrs={'rows': 3})
        }


class ChristianEducationLevelForm(forms.ModelForm):
    class Meta:
        model = ChristianEducationLevel
        fields = ['name', 'description', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ChristianCourseForm(forms.ModelForm):
    class Meta:
        model = ChristianCourse
        fields = [
            'title', 'description', 'level', 'category',
            'objectives', 'prerequisites', 'duration_weeks',
            'image', 'syllabus', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter course description'
            }),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'objectives': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter course objectives'
            }),
            'prerequisites': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter prerequisites (if any)'
            }),
            'duration_weeks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'syllabus': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ChristianModuleForm(forms.ModelForm):
    class Meta:
        model = ChristianModule
        fields = [
            'title', 'description', 'order', 'content',
            'scripture_references', 'learning_activities',
            'resources', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter module title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter module description'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Enter module content'
            }),
            'scripture_references': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter relevant scripture references'
            }),
            'learning_activities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter learning activities'
            }),
            'resources': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter additional resources'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ChristianAssignmentForm(forms.ModelForm):
    class Meta:
        model = ChristianAssignment
        fields = [
            'title', 'description', 'assignment_type',
            'due_date', 'points', 'instructions',
            'rubric', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter assignment title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter assignment description'
            }),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter assignment instructions'
            }),
            'rubric': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter grading rubric'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        points = cleaned_data.get('points')

        if points and points < 0:
            raise forms.ValidationError('Points cannot be negative.')

        return cleaned_data


class ChristianAssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = ChristianAssignmentSubmission
        fields = ['content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter your submission content'
            }),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ChristianGradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = ChristianAssignmentSubmission
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter feedback for the student'
            }),
        }


class ChristianDiscussionForm(forms.ModelForm):
    class Meta:
        model = ChristianDiscussion
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter discussion topic'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter discussion description'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ChristianDiscussionPostForm(forms.ModelForm):
    class Meta:
        model = ChristianDiscussionPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your response'
            }),
        }


class ChristianEnrollmentForm(forms.ModelForm):
    class Meta:
        model = ChristianEnrollment
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any additional notes'
            }),
        }


class ChristianEnrollmentUpdateForm(forms.ModelForm):
    class Meta:
        model = ChristianEnrollment
        fields = ['status', 'progress', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'progress': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'type': 'number'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter progress notes'
            }),
        }

    def clean_progress(self):
        progress = self.cleaned_data.get('progress')
        if progress is not None:
            if progress < 0:
                raise forms.ValidationError('Progress cannot be negative.')
            if progress > 100:
                raise forms.ValidationError('Progress cannot exceed 100%.')
        return


class TheologicalResourceForm(forms.ModelForm):
    class Meta:
        model = TheologicalResource
        fields = [
            'title', 'author', 'category', 'resource_type', 'level',
            'description', 'content', 'scripture_references', 'key_points',
            'publication_date', 'file', 'external_link', 'thumbnail',
            'is_featured', 'is_public', 'requires_permission'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'content': forms.Textarea(attrs={'rows': 8}),
            'key_points': forms.Textarea(attrs={'rows': 4}),
            'scripture_references': forms.Textarea(attrs={'rows': 2}),
            'publication_date': forms.DateInput(attrs={'type': 'date'})
        }


class StudyNoteForm(forms.ModelForm):
    class Meta:
        model = StudyNote
        fields = ['title', 'content', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class ResourceReviewForm(forms.ModelForm):
    class Meta:
        model = ResourceReview
        fields = [
            'rating', 'review_text', 'theological_accuracy',
            'clarity', 'practicality'
        ]
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4}),
        }


class BibliographyForm(forms.ModelForm):
    class Meta:
        model = Bibliography
        fields = ['title', 'authors', 'publication', 'year', 'pages', 'url']


class MaterialForm(forms.ModelForm):
    class Meta:
        model = SundaySchoolMaterial
        fields = [
            'title', 'age_group', 'category', 'description',
            'bible_reference', 'main_points', 'learning_objectives',
            'materials_needed', 'duration_minutes', 'content',
            'teacher_notes', 'image', 'attachment'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'main_points': forms.Textarea(attrs={'rows': 4}),
            'learning_objectives': forms.Textarea(attrs={'rows': 4}),
            'materials_needed': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 8}),
            'teacher_notes': forms.Textarea(attrs={'rows': 4}),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'title', 'description', 'instructions',
            'duration_minutes', 'materials_needed',
            'image', 'order'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 4}),
            'materials_needed': forms.Textarea(attrs={'rows': 3}),
        }


class TeachingResourceForm(forms.ModelForm):
    class Meta:
        model = TeachingResource
        fields = [
            'title', 'resource_type', 'description',
            'file', 'is_downloadable'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'rating', 'comment', 'used_date',
            'age_group_effectiveness', 'time_management',
            'student_engagement', 'suggestions'
        ]
        widgets = {
            'used_date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
            'suggestions': forms.Textarea(attrs={'rows': 3}),
        }


class LeadershipTrainingForm(forms.ModelForm):
    class Meta:
        model = LeadershipTraining
        fields = [
            'title', 'category', 'level', 'description',
            'learning_objectives', 'prerequisites', 'duration_weeks',
            'max_participants', 'mentor', 'image', 'syllabus'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'learning_objectives': forms.Textarea(attrs={'rows': 4}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
        }


class TrainingModuleForm(forms.ModelForm):
    class Meta:
        model = TrainingModule
        fields = ['title', 'description', 'order', 'competencies']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'competencies': forms.Textarea(attrs={'rows': 4}),
        }


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = [
            'title', 'content', 'practical_exercise',
            'reflection_questions', 'resources',
            'duration_minutes', 'order'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
            'practical_exercise': forms.Textarea(attrs={'rows': 4}),
            'reflection_questions': forms.Textarea(attrs={'rows': 4}),
            'resources': forms.Textarea(attrs={'rows': 3}),
        }


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = LeadershipAssessment
        fields = [
            'title', 'description', 'assessment_type',
            'criteria', 'passing_score', 'due_days'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'criteria': forms.Textarea(attrs={'rows': 4}),
        }


class LeadershipEnrollmentForm(forms.ModelForm):
    class Meta:
        model = ParticipantEnrollment
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Why do you want to join this training program?'
            }),
        }


class AssessmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssessmentSubmission
        fields = ['submission_text', 'evidence_file']
        widgets = {
            'submission_text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Enter your response here...'
            }),
        }

    def clean_evidence_file(self):
        file = self.cleaned_data.get('evidence_file')
        if file:
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('File size must be under 5MB')
            valid_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx']
            ext = file.name.lower()[-5:]
            if not any(ext.endswith(e) for e in valid_extensions):
                raise forms.ValidationError('Please upload a valid document file')
        return file


class AssessmentReviewForm(forms.ModelForm):
    class Meta:
        model = AssessmentSubmission
        fields = ['status', 'score', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score:
            passing_score = self.instance.assessment.passing_score
            if score > 100:
                raise forms.ValidationError('Score cannot exceed 100')
            if score < 0:
                raise forms.ValidationError('Score cannot be negative')
        return score


class MentorshipSessionForm(forms.ModelForm):
    class Meta:
        model = MentorshipSession
        fields = ['scheduled_date', 'duration_minutes', 'topics']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'topics': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Topics to be covered in this session...'
            }),
        }


class MentorshipFeedbackForm(forms.ModelForm):
    class Meta:
        model = MentorshipSession
        fields = ['completed', 'notes', 'feedback']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }


class BiblicalCourseForm(forms.ModelForm):
    class Meta:
        model = BiblicalCourse
        fields = ['title', 'description', 'level', 'duration_weeks',
                  'prerequisites', 'image', 'syllabus', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
        }


class CourseModuleForm(forms.ModelForm):
    class Meta:
        model = CourseModule
        fields = ['title', 'description', 'order', 'learning_objectives']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'learning_objectives': forms.Textarea(attrs={'rows': 4}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'scripture_references', 'video_url',
                  'audio_file', 'presentation', 'additional_resources',
                  'order', 'duration_minutes']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'class': 'rich-text-editor'}),
            'scripture_references': forms.Textarea(attrs={'rows': 3}),
            'additional_resources': forms.Textarea(attrs={'rows': 4}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_days', 'points']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['submission_text', 'file_upload']
        widgets = {
            'submission_text': forms.Textarea(attrs={'rows': 6}),
        }


class AssignmentGradingForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['grade', 'feedback', 'status']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class DiscussionReplyForm(forms.ModelForm):
    class Meta:
        model = DiscussionReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }


class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = StudentEnrollment
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
