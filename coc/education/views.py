from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.db.models import Avg
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView
)

from . import models
from .forms import (BiblicalCourseForm, AssignmentSubmissionForm, AssignmentGradingForm,
                    DiscussionForm, DiscussionReplyForm, StudentEnrollmentForm, TheologicalResourceForm)
from .forms import (
    ChristianEducationLevelForm, ChristianCourseForm, ChristianModuleForm,
    ChristianAssignmentForm, ChristianAssignmentSubmissionForm,
    ChristianGradeSubmissionForm, ChristianDiscussionForm,
    ChristianDiscussionPostForm, ChristianEnrollmentForm,
    ChristianEnrollmentUpdateForm
)
from .forms import (
    LeadershipEnrollmentForm, AssessmentSubmissionForm
)
from .forms import (
    LeadershipTrainingForm, AssessmentReviewForm, MentorshipFeedbackForm
)
from .forms import MaterialForm, ActivityForm, FeedbackForm
from .forms import (
    StudyNoteForm, ResourceReviewForm
)
from .models import (BiblicalCourse, Lesson, Assignment,
                     StudentEnrollment, AssignmentSubmission, Discussion, ChristianMentorshipFeedback)
from .models import (
    ChristianEducationLevel, ChristianCourse, ChristianModule,
    ChristianAssignment, ChristianAssignmentSubmission,
    ChristianDiscussion, ChristianDiscussionPost, ChristianEnrollment
)
from .models import (
    LeadershipTraining, ParticipantEnrollment,
    AssessmentSubmission, MentorshipSession
)
from .models import SundaySchoolMaterial, AgeGroup
from .models import (
    TheologicalResource, TheologicalCategory,
    StudyNote, ResourceReview
)
from .models import (
    TrainingSession,
    LeadershipAssessment
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import (
    ChristianMentorshipSession,
    ChristianMentorProfile,
    ChristianMentorshipApplication
)
from .forms import (
    ChristianMentorshipSessionForm,
    ChristianMentorshipApplicationForm,
    ChristianMentorshipFeedbackForm
)
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from .models import (
    BibleCollegeProgram, BibleCollegeCourse, BibleCollegeStudent,
    BibleCollegeEnrollment, BibleCollegeAssignment, BibleCollegeSubmission
)
from .forms import (
    BibleCollegeProgramForm, BibleCollegeCourseForm, BibleCollegeStudentForm,
    BibleCollegeEnrollmentForm, BibleCollegeAssignmentForm, BibleCollegeSubmissionForm,
    BibleCollegeGradeForm
)


# Program Views
@login_required
def bible_college_program_list(request):
    programs = BibleCollegeProgram.objects.filter(is_active=True)
    return render(request, 'education/bible_college/program_list.html', {
        'programs': programs
    })


@login_required
def bible_college_program_detail(request, program_id):
    program = get_object_or_404(BibleCollegeProgram, id=program_id)
    courses = program.bible_college_courses.all().order_by('year_level', 'semester')
    return render(request, 'education/bible_college/program_detail.html', {
        'program': program,
        'courses': courses
    })


# Course Views
@login_required
def bible_college_course_list(request):
    student = get_object_or_404(BibleCollegeStudent, user=request.user)
    enrollments = student.bible_college_enrollments.filter(completed=False)
    available_courses = BibleCollegeCourse.objects.filter(
        program=student.program,
        year_level=student.current_year
    )
    return render(request, 'education/bible_college/course_list.html', {
        'enrollments': enrollments,
        'available_courses': available_courses
    })


@login_required
def bible_college_course_detail(request, course_id):
    course = get_object_or_404(BibleCollegeCourse, id=course_id)
    student = get_object_or_404(BibleCollegeStudent, user=request.user)
    enrollment = BibleCollegeEnrollment.objects.filter(
        student=student,
        course=course
    ).first()
    assignments = course.bible_college_assignments.all()
    return render(request, 'education/bible_college/course_detail.html', {
        'course': course,
        'enrollment': enrollment,
        'assignments': assignments
    })


# Student Views
@login_required
def bible_college_dashboard(request):
    try:
        student = request.user.bible_college_student
        enrollments = student.bible_college_enrollments.filter(completed=False)
        assignments = BibleCollegeAssignment.objects.filter(
            course__in=enrollments.values_list('course', flat=True)
        ).order_by('due_date')
        return render(request, 'education/bible_college/dashboard.html', {
            'student': student,
            'enrollments': enrollments,
            'assignments': assignments
        })
    except BibleCollegeStudent.DoesNotExist:
        return redirect('education:bible_college_register')


@login_required
def bible_college_register(request):
    if hasattr(request.user, 'bible_college_student'):
        return redirect('education:bible_college_dashboard')

    if request.method == 'POST':
        form = BibleCollegeStudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.enrollment_date = timezone.now().date()
            student.save()
            messages.success(request, 'Successfully registered for Bible College!')
            return redirect('education:bible_college_dashboard')
    else:
        form = BibleCollegeStudentForm()

    return render(request, 'education/bible_college/register.html', {'form': form})


# Assignment Views
@login_required
def bible_college_submit_assignment(request, assignment_id):
    assignment = get_object_or_404(BibleCollegeAssignment, id=assignment_id)
    student = request.user.bible_college_student

    try:
        submission = BibleCollegeSubmission.objects.get(
            assignment=assignment,
            student=student
        )
    except BibleCollegeSubmission.DoesNotExist:
        submission = None

    if request.method == 'POST':
        form = BibleCollegeSubmissionForm(
            request.POST,
            request.FILES,
            instance=submission
        )
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = student
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('education:bible_college_course_detail',
                            course_id=assignment.course.id)
    else:
        form = BibleCollegeSubmissionForm(instance=submission)

    return render(request, 'education/bible_college/submit_assignment.html', {
        'form': form,
        'assignment': assignment,
        'submission': submission
    })


def mentorship_guidelines(request):
    return render(request, 'education/leadership/guidelines.html')


@login_required
@permission_required('education.add_christianmentorshipsession', raise_exception=True)
def create_mentorship_session(request):
    mentor_profile = get_object_or_404(ChristianMentorProfile, user=request.user)

    if request.method == 'POST':
        form = ChristianMentorshipSessionForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save(commit=False)
            session.mentor = mentor_profile
            session.status = 'scheduled'
            session.save()

            messages.success(request, 'Mentorship session created successfully!')
            return redirect('education:mentorship_session_list')
    else:
        form = ChristianMentorshipSessionForm()

    return render(request, 'education/leadership/session_create.html', {
        'form': form
    })


@login_required
def mentor_profile(request, mentor_id):
    mentor = get_object_or_404(ChristianMentorProfile, pk=mentor_id)
    upcoming_sessions = ChristianMentorshipSession.objects.filter(
        mentor=mentor,
        date__gte=timezone.now().date(),
        status='scheduled'
    )
    testimonials = ChristianMentorshipFeedback.objects.filter(
        session__mentor=mentor
    ).order_by('-created_at')[:5]

    context = {
        'mentor': mentor,
        'upcoming_sessions': upcoming_sessions,
        'testimonials': testimonials
    }
    return render(request, 'education/mentorship/mentor_profile.html', context)


@login_required
def christian_mentorship_session_list(request):
    upcoming_sessions = ChristianMentorshipSession.objects.filter(
        date__gte=timezone.now().date(),
        status='scheduled'
    )
    past_sessions = ChristianMentorshipSession.objects.filter(
        date__lt=timezone.now().date()
    )
    featured_mentors = ChristianMentorProfile.objects.filter(
        accepting_mentees=True
    )[:5]

    context = {
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
        'featured_mentors': featured_mentors,
        'max_participants': ChristianMentorshipSession._meta.get_field('max_participants').default
    }
    return render(request, 'education/mentorship/session_list.html', context)


@login_required
def register_for_christian_session(request, session_id):
    session = get_object_or_404(ChristianMentorshipSession, pk=session_id)

    if request.method == 'POST':
        if session.is_full:
            messages.error(request, 'This mentorship session is already full.')
        else:
            session.participants.add(request.user)
            messages.success(request, 'Successfully registered for the Christian mentorship session.')

    return redirect('education:session_list')


@login_required
def apply_for_christian_mentorship(request, mentor_id):
    mentor = get_object_or_404(ChristianMentorProfile, pk=mentor_id)

    if request.method == 'POST':
        form = ChristianMentorshipApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.mentor = mentor
            application.save()
            messages.success(request, 'Your Christian mentorship application has been submitted.')
            return redirect('education:mentor_profile', pk=mentor_id)
    else:
        form = ChristianMentorshipApplicationForm()

    return render(request, 'education/mentorship/application_form.html', {
        'form': form,
        'mentor': mentor
    })


@login_required
def submit_christian_session_feedback(request, session_id):
    session = get_object_or_404(ChristianMentorshipSession, pk=session_id)

    if request.method == 'POST':
        form = ChristianMentorshipFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.session = session
            feedback.participant = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback on the mentorship session!')
            return redirect('education:session_list')
    else:
        form = ChristianMentorshipFeedbackForm()

    return render(request, 'education/mentorship/feedback_form.html', {
        'form': form,
        'session': session
    })


# Education Level Views
class ChristianEducationLevelListView(ListView):
    model = ChristianEducationLevel
    template_name = 'education/christian_education/level_list.html'
    context_object_name = 'levels'
    ordering = ['order', 'name']


class ChristianEducationLevelDetailView(DetailView):
    model = ChristianEducationLevel
    template_name = 'education/christian_education/level_detail.html'
    context_object_name = 'level'


class ChristianEducationLevelCreateView(PermissionRequiredMixin, CreateView):
    model = ChristianEducationLevel
    form_class = ChristianEducationLevelForm
    template_name = 'education/christian_education/level_form.html'
    permission_required = 'coc.add_christianeducationlevel'
    success_url = reverse_lazy('education:education_level_list')


class ChristianEducationLevelUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChristianEducationLevel
    form_class = ChristianEducationLevelForm
    template_name = 'education/christian_education/level_form.html'
    permission_required = 'coc.change_christianeducationlevel'


class ChristianEducationLevelDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChristianEducationLevel
    template_name = 'education/christian_education/level_confirm_delete.html'
    permission_required = 'coc.delete_christianeducationlevel'
    success_url = reverse_lazy('education:education_level_list')


# Course Views
class ChristianCourseListView(ListView):
    model = ChristianCourse
    template_name = 'education/christian_education/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('coc.view_inactive_courses'):
            queryset = queryset.filter(is_active=True)
        return queryset


class ChristianCourseDetailView(DetailView):
    model = ChristianCourse
    template_name = 'education/christian_education/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['enrollment'] = ChristianEnrollment.objects.filter(
                course=self.object,
                student=self.request.user
            ).first()
        return context


class ChristianCourseCreateView(PermissionRequiredMixin, CreateView):
    model = ChristianCourse
    form_class = ChristianCourseForm
    template_name = 'education/christian_education/course_form.html'
    permission_required = 'coc.add_christiancourse'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)


class ChristianCourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChristianCourse
    form_class = ChristianCourseForm
    template_name = 'education/christian_education/course_form.html'
    permission_required = 'coc.change_christiancourse'


class ChristianCourseDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChristianCourse
    template_name = 'education/christian_education/course_confirm_delete.html'
    permission_required = 'coc.delete_christiancourse'
    success_url = reverse_lazy('education:course_list')


# Module Views
class ChristianModuleListView(ListView):
    model = ChristianModule
    template_name = 'education/christian_education/module_list.html'
    context_object_name = 'modules'

    def get_queryset(self):
        self.course = get_object_or_404(ChristianCourse, slug=self.kwargs['course_slug'])
        return ChristianModule.objects.filter(course=self.course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context


class ChristianModuleDetailView(DetailView):
    model = ChristianModule
    template_name = 'education/christian_education/module_detail.html'
    context_object_name = 'module'


class ChristianModuleCreateView(PermissionRequiredMixin, CreateView):
    model = ChristianModule
    form_class = ChristianModuleForm
    template_name = 'education/christian_education/module_form.html'
    permission_required = 'coc.add_christianmodule'

    def form_valid(self, form):
        course = get_object_or_404(ChristianCourse, slug=self.kwargs['course_slug'])
        form.instance.course = course
        return super().form_valid(form)


class ChristianModuleUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChristianModule
    form_class = ChristianModuleForm
    template_name = 'education/christian_education/module_form.html'
    permission_required = 'coc.change_christianmodule'


class ChristianModuleDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChristianModule
    template_name = 'education/christian_education/module_confirm_delete.html'
    permission_required = 'coc.delete_christianmodule'

    def get_success_url(self):
        return reverse_lazy('education:module_list',
                            kwargs={'course_slug': self.object.course.slug})


# Assignment Views
class ChristianAssignmentListView(ListView):
    model = ChristianAssignment
    template_name = 'education/christian_education/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        self.module = get_object_or_404(ChristianModule, pk=self.kwargs['module_pk'])
        return ChristianAssignment.objects.filter(module=self.module)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        return context


class ChristianAssignmentDetailView(DetailView):
    model = ChristianAssignment
    template_name = 'education/christian_education/assignment_detail.html'
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['submission'] = ChristianAssignmentSubmission.objects.filter(
                assignment=self.object,
                student=self.request.user
            ).first()
        return context


class ChristianAssignmentCreateView(PermissionRequiredMixin, CreateView):
    model = ChristianAssignment
    form_class = ChristianAssignmentForm
    template_name = 'education/christian_education/assignment_form.html'
    permission_required = 'coc.add_christianassignment'

    def form_valid(self, form):
        module = get_object_or_404(ChristianModule, pk=self.kwargs['module_pk'])
        form.instance.module = module
        return super().form_valid(form)


class ChristianAssignmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChristianAssignment
    form_class = ChristianAssignmentForm
    template_name = 'education/christian_education/assignment_form.html'
    permission_required = 'coc.change_christianassignment'


class ChristianAssignmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChristianAssignment
    template_name = 'education/christian_education/assignment_confirm_delete.html'
    permission_required = 'coc.delete_christianassignment'

    def get_success_url(self):
        return reverse_lazy('christian_education:assignment_list',
                            kwargs={'module_pk': self.object.module.pk})


# Assignment Submission Views
class ChristianAssignmentSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = ChristianAssignmentSubmission
    form_class = ChristianAssignmentSubmissionForm
    template_name = 'education/christian_education/submission_form.html'

    def form_valid(self, form):
        assignment = get_object_or_404(ChristianAssignment, pk=self.kwargs['assignment_pk'])
        form.instance.assignment = assignment
        form.instance.student = self.request.user
        return super().form_valid(form)


class ChristianAssignmentSubmissionDetailView(LoginRequiredMixin, DetailView):
    model = ChristianAssignmentSubmission
    template_name = 'education/christian_education/submission_detail.html'
    context_object_name = 'submission'


class ChristianGradeSubmissionUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChristianAssignmentSubmission
    form_class = ChristianGradeSubmissionForm
    template_name = 'education/christian_education/grade_submission_form.html'
    permission_required = 'coc.grade_christianassignmentsubmission'

    def form_valid(self, form):
        form.instance.graded_by = self.request.user
        form.instance.graded_date = timezone.now()
        return super().form_valid(form)


# Discussion Views
class ChristianDiscussionListView(ListView):
    model = ChristianDiscussion
    template_name = 'education/christian_education/discussion_list.html'
    context_object_name = 'discussions'

    def get_queryset(self):
        self.module = get_object_or_404(ChristianModule, pk=self.kwargs['module_pk'])
        return ChristianDiscussion.objects.filter(module=self.module)


class ChristianDiscussionDetailView(DetailView):
    model = ChristianDiscussion
    template_name = 'education/christian_education/discussion_detail.html'
    context_object_name = 'discussion'


class ChristianDiscussionCreateView(PermissionRequiredMixin, CreateView):
    model = ChristianDiscussion
    form_class = ChristianDiscussionForm
    template_name = 'education/christian_education/discussion_form.html'
    permission_required = 'coc.add_christiandiscussion'

    def form_valid(self, form):
        module = get_object_or_404(ChristianModule, pk=self.kwargs['module_pk'])
        form.instance.module = module
        return super().form_valid(form)


class ChristianDiscussionUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChristianDiscussion
    form_class = ChristianDiscussionForm
    template_name = 'education/christian_education/discussion_form.html'
    permission_required = 'coc.change_christiandiscussion'


class ChristianDiscussionDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChristianDiscussion
    template_name = 'education/christian_education/discussion_confirm_delete.html'
    permission_required = 'coc.delete_christiandiscussion'

    def get_success_url(self):
        return reverse_lazy('education:discussion_list',
                            kwargs={'module_pk': self.object.module.pk})


# Discussion Post Views
class ChristianDiscussionPostCreateView(LoginRequiredMixin, CreateView):
    model = ChristianDiscussionPost
    form_class = ChristianDiscussionPostForm
    template_name = 'education/christian_education/post_form.html'

    def form_valid(self, form):
        discussion = get_object_or_404(ChristianDiscussion, pk=self.kwargs['discussion_pk'])
        form.instance.discussion = discussion
        form.instance.author = self.request.user
        return super().form_valid(form)


class ChristianDiscussionPostDetailView(DetailView):
    model = ChristianDiscussionPost
    template_name = 'education/christian_education/post_detail.html'
    context_object_name = 'post'


class ChristianDiscussionPostUpdateView(LoginRequiredMixin, UpdateView):
    model = ChristianDiscussionPost
    form_class = ChristianDiscussionPostForm
    template_name = 'education/christian_education/post_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class ChristianDiscussionPostDeleteView(LoginRequiredMixin, DeleteView):
    model = ChristianDiscussionPost
    template_name = 'education/christian_education/post_confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('education:discussion_detail',
                            kwargs={'pk': self.object.discussion.pk})


class ChristianDiscussionPostReplyView(LoginRequiredMixin, CreateView):
    model = ChristianDiscussionPost
    form_class = ChristianDiscussionPostForm
    template_name = 'education/christian_education/post_form.html'

    def form_valid(self, form):
        parent_post = get_object_or_404(ChristianDiscussionPost, pk=self.kwargs['pk'])
        form.instance.discussion = parent_post.discussion
        form.instance.parent = parent_post
        form.instance.author = self.request.user
        return super().form_valid(form)


# Enrollment Views
class ChristianEnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = ChristianEnrollment
    form_class = ChristianEnrollmentForm
    template_name = 'education/christian_education/enrollment_form.html'

    def form_valid(self, form):
        course = get_object_or_404(ChristianCourse, slug=self.kwargs['course_slug'])
        form.instance.course = course
        form.instance.student = self.request.user
        return super().form_valid(form)


class ChristianEnrollmentListView(LoginRequiredMixin, ListView):
    model = ChristianEnrollment
    template_name = 'education/christian_education/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return ChristianEnrollment.objects.filter(student=self.request.user)


class ChristianEnrollmentDetailView(LoginRequiredMixin, DetailView):
    model = ChristianEnrollment
    template_name = 'education/christian_education/enrollment_detail.html'
    context_object_name = 'enrollment'


class ChristianEnrollmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChristianEnrollment
    form_class = ChristianEnrollmentUpdateForm
    template_name = 'education/christian_education/enrollment_form.html'
    permission_required = 'coc.change_christianenrollment'


class ChristianEnrollmentDeleteView(LoginRequiredMixin, DeleteView):
    model = ChristianEnrollment
    template_name = 'education/christian_education/enrollment_confirm_delete.html'
    success_url = reverse_lazy('education:enrollment_list')

    def get_queryset(self):
        return super().get_queryset().filter(student=self.request.user)


# Dashboard Views
class ChristianEducationStudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'education/christian_education/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = ChristianEnrollment.objects.filter(
            student=self.request.user
        ).select_related('course')
        return context


class ChristianEducationInstructorDashboardView(PermissionRequiredMixin, TemplateView):
    template_name = 'education/christian_education/instructor_dashboard.html'
    permission_required = 'coc.view_instructor_dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = ChristianCourse.objects.filter(instructor=self.request.user)
        return context


# API Views
def update_module_progress(request, pk):
    if request.method == 'POST' and request.is_ajax():
        module = get_object_or_404(ChristianModule, pk=pk)
        enrollment = get_object_or_404(
            ChristianEnrollment,
            course=module.course,
            student=request.user
        )
        progress = request.POST.get('progress')
        if progress and progress.isdigit():
            enrollment.progress = int(progress)
            enrollment.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def load_discussion_posts(request, pk):
    discussion = get_object_or_404(ChristianDiscussion, pk=pk)
    posts = ChristianDiscussionPost.objects.filter(
        discussion=discussion,
        parent=None
    ).select_related('author')
    data = [{
        'id': post.id,
        'content': post.content,
        'author': post.author.get_full_name(),
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'replies': list(post.replies.values('id', 'content', 'author__first_name'))
    } for post in posts]
    return JsonResponse({'posts': data})


def resource_list(request):
    categories = TheologicalCategory.objects.all()
    resources = TheologicalResource.objects.filter(is_public=True)

    # Apply filters
    category = request.GET.get('category')
    level = request.GET.get('level')
    resource_type = request.GET.get('type')
    query = request.GET.get('q')

    if category:
        resources = resources.filter(category__slug=category)
    if level:
        resources = resources.filter(level=level)
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__icontains=query)
        )

    context = {
        'resources': resources,
        'categories': categories,
        'levels': TheologicalResource.LEVEL_CHOICES,
        'types': TheologicalResource.TYPE_CHOICES
    }
    return render(request, 'education/theological/resource_list.html', context)


def resource_detail(request, slug):
    resource = get_object_or_404(TheologicalResource, slug=slug)
    reviews = ResourceReview.objects.filter(
        resource=resource,
        is_approved=True
    ).select_related('user').order_by('-created_at')

    # Get cached ratings or calculate if not cached
    cache_key = f'resource_ratings_{resource.id}'
    ratings = cache.get(cache_key)

    if not ratings:
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        avg_accuracy = reviews.aggregate(Avg('theological_accuracy'))['theological_accuracy__avg'] or 0
        avg_clarity = reviews.aggregate(Avg('clarity'))['clarity__avg'] or 0
        avg_practicality = reviews.aggregate(Avg('practicality'))['practicality__avg'] or 0

        ratings = {
            'avg_rating': round(avg_rating, 1),
            'avg_accuracy': round(avg_accuracy, 1),
            'avg_clarity': round(avg_clarity, 1),
            'avg_practicality': round(avg_practicality, 1),
            'review_count': reviews.count()
        }
        cache.set(cache_key, ratings, timeout=86400)

    # Get user's review if exists
    user_review = None
    if request.user.is_authenticated:
        user_review = ResourceReview.objects.filter(
            resource=resource,
            user=request.user
        ).first()

    # Get study notes
    if request.user.is_authenticated:
        study_notes = StudyNote.objects.filter(
            resource=resource,
            user=request.user
        ).order_by('-created_at')
    else:
        study_notes = None

    context = {
        'resource': resource,
        'reviews': reviews,
        'ratings': ratings,
        'user_review': user_review,
        'study_notes': study_notes,
    }
    return render(request, 'education/theological/resource_detail.html', context)


@login_required
@permission_required('coc.add_theologicalresource')
def create_resource(request):
    if request.method == 'POST':
        form = TheologicalResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()
            messages.success(request, 'Resource created successfully!')
            return redirect('education:resource_detail', slug=resource.slug)
    else:
        form = TheologicalResourceForm()

    return render(request, 'education/theological/resource_form.html', {'form': form})


@login_required
def add_study_note(request, resource_slug):
    resource = get_object_or_404(TheologicalResource, slug=resource_slug)

    if request.method == 'POST':
        form = StudyNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.resource = resource
            note.user = request.user
            note.save()
            messages.success(request, 'Study note added successfully!')
            return redirect('education:resource_detail', slug=resource_slug)
    else:
        form = StudyNoteForm()

    return render(request, 'education/theological/study_note_form.html', {
        'form': form,
        'resource': resource
    })


@login_required
def add_review(request, resource_slug):
    resource = get_object_or_404(TheologicalResource, slug=resource_slug)

    # Check if user already reviewed
    existing_review = ResourceReview.objects.filter(
        resource=resource,
        user=request.user
    ).first()

    if request.method == 'POST':
        form = ResourceReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.resource = resource
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('education:resource_detail', slug=resource_slug)
    else:
        form = ResourceReviewForm(instance=existing_review)

    return render(request, 'education/theological/review_form.html', {
        'form': form,
        'resource': resource,
        'is_update': existing_review is not None
    })


def material_list(request):
    age_group = request.GET.get('age_group')
    category = request.GET.get('category')

    materials = SundaySchoolMaterial.objects.filter(is_active=True)

    if age_group:
        materials = materials.filter(age_group_id=age_group)
    if category:
        materials = materials.filter(category=category)

    context = {
        'materials': materials,
        'age_groups': AgeGroup.objects.all(),
        'categories': SundaySchoolMaterial.CATEGORY_CHOICES,
    }
    return render(request, 'education/sunday_school/material_list.html', context)


@login_required
def material_detail(request, slug):
    material = get_object_or_404(SundaySchoolMaterial, slug=slug)
    activities = material.activity_set.all()
    resources = material.teachingresource_set.all()
    feedback = material.feedback_set.all()

    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.material = material
            feedback.teacher = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('education:material_detail', slug=slug)
    else:
        feedback_form = FeedbackForm()

    context = {
        'material': material,
        'activities': activities,
        'resources': resources,
        'feedback': feedback,
        'feedback_form': feedback_form,
    }
    return render(request, 'education/sunday_school/material_detail.html', context)


@login_required
def create_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.created_by = request.user
            material.save()
            messages.success(request, 'Material created successfully!')
            return redirect('education:material_detail', slug=material.slug)
    else:
        form = MaterialForm()

    return render(request, 'education/sunday_school/material_form.html', {'form': form})


@login_required
def add_activity(request, material_slug):
    material = get_object_or_404(SundaySchoolMaterial, slug=material_slug)

    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.material = material
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('education:material_detail', slug=material_slug)
    else:
        form = ActivityForm()

    return render(request, 'education/sunday_school/activity_form.html', {
        'form': form,
        'material': material
    })


@login_required
def training_list(request):
    trainings = LeadershipTraining.objects.filter(is_active=True)

    # Apply filters if provided
    category = request.GET.get('category')
    level = request.GET.get('level')

    if category:
        trainings = trainings.filter(category=category)
    if level:
        trainings = trainings.filter(level=level)

    # Get enrolled trainings for user
    enrolled_trainings = None
    if request.user.is_authenticated:
        enrolled_trainings = LeadershipTraining.objects.filter(
            participantenrollment__participant=request.user
        ).select_related('mentor')

    context = {
        'trainings': trainings.select_related('mentor'),
        'enrolled_trainings': enrolled_trainings,
        'categories': LeadershipTraining.CATEGORY_CHOICES,
        'levels': LeadershipTraining.LEVEL_CHOICES,
    }

    return render(request, 'education/leadership/training_list.html', context)


@login_required
def training_detail(request, slug):
    training = get_object_or_404(LeadershipTraining, slug=slug)

    # Get enrollment if exists
    enrollment = None
    sessions_completed = 0
    if request.user.is_authenticated:
        enrollment = ParticipantEnrollment.objects.filter(
            participant=request.user,
            training=training
        ).first()

        if enrollment and enrollment.status == 'active':
            sessions_completed = AssessmentSubmission.objects.filter(
                participant=request.user,
                assessment__session__module__training=training,
                status='reviewed',
                score__gte=F('assessment__passing_score')
            ).count()

    context = {
        'training': training,
        'enrollment': enrollment,
        'sessions_completed': sessions_completed,
    }

    return render(request, 'education/leadership/training_detail.html', context)


@login_required
def enroll_training(request, slug):
    training = get_object_or_404(LeadershipTraining, slug=slug)

    # Check if already enrolled
    existing_enrollment = ParticipantEnrollment.objects.filter(
        participant=request.user,
        training=training
    ).exists()

    if existing_enrollment:
        messages.error(request, 'You are already enrolled in this training.')
        return redirect('education:training_detail', slug=slug)

    # Check if training is full
    if training.participantenrollment_set.count() >= training.max_participants:
        messages.error(request, 'This training program is full.')
        return redirect('education:training_detail', slug=slug)

    if request.method == 'POST':
        form = LeadershipEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.participant = request.user
            enrollment.training = training
            enrollment.save()

            messages.success(request, 'Your enrollment application has been submitted.')
            return redirect('education:training_detail', slug=slug)
    else:
        form = LeadershipEnrollmentForm()

    context = {
        'form': form,
        'training': training,
    }

    return render(request, 'education/leadership/enroll_training.html', context)


@login_required
def mentorship_session_detail(request, pk):
    session = get_object_or_404(MentorshipSession, pk=pk)

    if request.method == 'POST' and request.user == session.mentor:
        form = MentorshipFeedbackForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session feedback saved successfully.")
            return redirect('education:mentorship_session_detail', pk=pk)
    else:
        form = MentorshipFeedbackForm(instance=session) if request.user == session.mentor else None

    context = {
        'session': session,
        'feedback_form': form,
    }

    return render(request, 'education/leadership/mentorship_session_detail.html', context)


class StaffRequiredMixin(UserPassesTestMixin):
    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.is_staff


class MentorshipSessionDetailView(LoginRequiredMixin, DetailView):
    model = MentorshipSession
    template_name = 'education/leadership/mentorship_session_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.object.mentor:
            context['feedback_form'] = MentorshipFeedbackForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        if request.user != self.get_object().mentor:
            messages.error(request, "You don't have permission to update this session.")
            return redirect('education:mentorship_sessions')

        form = MentorshipFeedbackForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, "Session feedback saved successfully.")
        return redirect('leadership:mentorship_session_detail', pk=self.get_object().pk)


class CreateTrainingView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = LeadershipTraining
    form_class = LeadershipTrainingForm
    template_name = 'education/leadership/training_form.html'
    success_url = reverse_lazy('education:training_list')

    def form_valid(self, form):
        messages.success(self.request, 'Training program created successfully!')
        return super().form_valid(form)


class UpdateTrainingView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = LeadershipTraining
    form_class = LeadershipTrainingForm
    template_name = 'education/leadership/training_form.html'

    def get_success_url(self):
        return reverse_lazy('education:training_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Training program updated successfully!')
        return super().form_valid(form)


class TrainingEnrollmentListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = ParticipantEnrollment
    template_name = 'education/leadership/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        self.training = get_object_or_404(LeadershipTraining, slug=self.kwargs['slug'])
        return ParticipantEnrollment.objects.filter(
            training=self.training
        ).select_related('participant')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training'] = self.training
        return context


class ReviewEnrollmentView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = ParticipantEnrollment
    template_name = 'education/leadership/review_enrollment.html'
    fields = ['status', 'notes']

    def form_valid(self, form):
        enrollment = form.save(commit=False)
        if enrollment.status == 'active':
            enrollment.approval_date = timezone.now()
            enrollment.approved_by = self.request.user
        enrollment.save()

        # Send notification to participant
        status_display = enrollment.get_status_display()
        messages.success(
            self.request,
            f'Enrollment status updated to {status_display} successfully!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'education:training_enrollments',
            kwargs={'slug': self.object.training.slug}
        )


class ReviewAssessmentView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = AssessmentSubmission
    form_class = AssessmentReviewForm
    template_name = 'education/leadership/review_assessment.html'

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.reviewed_by = self.request.user
        submission.reviewed_date = timezone.now()
        submission.save()

        # Update session completion if needed
        if submission.status == 'reviewed' and submission.score >= submission.assessment.passing_score:
            # Logic to mark session as completed
            pass

        messages.success(self.request, 'Assessment review submitted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'education:session_detail',
            kwargs={'pk': self.object.assessment.session.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission'] = self.object
        context['assessment'] = self.object.assessment
        return context


from django.views.generic import ListView
from django.db.models import Q
from .models import LeadershipTraining


class LeadershipTrainingListView(ListView):
    model = LeadershipTraining
    template_name = 'education/leadership/training_list.html'
    context_object_name = 'trainings'

    def get_queryset(self):
        queryset = LeadershipTraining.objects.filter(is_active=True)

        # Apply filters if provided
        category = self.request.GET.get('category')
        level = self.request.GET.get('level')

        if category:
            queryset = queryset.filter(category=category)
        if level:
            queryset = queryset.filter(level=level)

        return queryset.select_related('mentor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add filter choices
        context['categories'] = LeadershipTraining.CATEGORY_CHOICES
        context['levels'] = LeadershipTraining.LEVEL_CHOICES

        # Get enrolled trainings for authenticated user
        if self.request.user.is_authenticated:
            context['enrolled_trainings'] = LeadershipTraining.objects.filter(
                participantenrollment__participant=self.request.user
            ).select_related('mentor')

        return context


class LeadershipTrainingDetailView(DetailView):
    model = LeadershipTraining
    template_name = 'education/leadership/training_detail.html'  # Updated template path
    context_object_name = 'training'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['enrollment'] = ParticipantEnrollment.objects.filter(
                participant=self.request.user,
                training=self.object
            ).first()
            if context['enrollment'] and context['enrollment'].status == 'active':
                context['sessions_completed'] = AssessmentSubmission.objects.filter(
                    participant=self.request.user,
                    assessment__session__module__training=self.object,
                    status='reviewed',
                    score__gte=models.F('assessment__passing_score')
                ).count()
        return context


class EnrollTrainingView(LoginRequiredMixin, CreateView):
    model = ParticipantEnrollment
    form_class = LeadershipEnrollmentForm
    template_name = 'education/leadership/enroll_training.html'

    def get_success_url(self):
        return reverse_lazy('education:training_detail',
                            kwargs={'slug': self.object.training.slug})

    def form_valid(self, form):
        form.instance.participant = self.request.user
        form.instance.training = get_object_or_404(
            LeadershipTraining,
            slug=self.kwargs['slug']
        )
        messages.success(self.request, 'Enrollment request submitted successfully!')
        return super().form_valid(form)


class TrainingSessionDetailView(LoginRequiredMixin, DetailView):
    model = TrainingSession
    template_name = 'education/leadership/session_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessments'] = self.object.leadershipassessment_set.all()
        context['submissions'] = AssessmentSubmission.objects.filter(
            participant=self.request.user,
            assessment__session=self.object
        )
        return context


class SubmitAssessmentView(LoginRequiredMixin, CreateView):
    model = AssessmentSubmission
    form_class = AssessmentSubmissionForm
    template_name = 'education/leadership/submit_assessment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessment'] = get_object_or_404(
            LeadershipAssessment,
            pk=self.kwargs['assessment_pk']
        )
        return context

    def form_valid(self, form):
        form.instance.participant = self.request.user
        form.instance.assessment_id = self.kwargs['assessment_pk']
        messages.success(self.request, 'Assessment submitted successfully!')
        return super().form_valid(form)


class MentorshipSessionListView(LoginRequiredMixin, ListView):
    model = MentorshipSession
    template_name = 'education/leadership/mentorship_sessions.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        if self.request.user.is_staff:
            return MentorshipSession.objects.filter(mentor=self.request.user)
        return MentorshipSession.objects.filter(participant=self.request.user)


class CourseListView(ListView):
    model = BiblicalCourse
    template_name = 'education/courses/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return BiblicalCourse.objects.filter(is_active=True)


class CourseDetailView(DetailView):
    model = BiblicalCourse
    template_name = 'education/courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['enrollment'] = StudentEnrollment.objects.filter(
                student=self.request.user,
                course=self.object
            ).first()
        return context


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(BiblicalCourse, slug=slug)

    if request.method == 'POST':
        form = StudentEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.course = course
            enrollment.save()
            messages.success(request, f'Successfully enrolled in {course.title}')
            return redirect('education:course_detail', slug=slug)
    else:
        form = StudentEnrollmentForm()

    return render(request, 'education/courses/enroll_course.html', {
        'form': form,
        'course': course
    })


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'education/courses/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progress'] = self.object.lessonprogress_set.filter(
            student=self.request.user
        ).first()
        context['assignments'] = self.object.assignments.all()
        context['discussions'] = self.object.discussions.all()
        return context


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('lesson_detail', pk=assignment.lesson.id)
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'education/courses/submit_assignment.html', {
        'form': form,
        'assignment': assignment
    })


class DiscussionCreateView(LoginRequiredMixin, CreateView):
    model = Discussion
    form_class = DiscussionForm
    template_name = 'education/courses/discussion_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.lesson_id = self.kwargs['lesson_id']
        return super().form_valid(form)


@login_required
def add_discussion_reply(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    if request.method == 'POST':
        form = DiscussionReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.discussion = discussion
            reply.created_by = request.user
            reply.save()
            return redirect('discussion_detail', pk=discussion_id)
    else:
        form = DiscussionReplyForm()

    return render(request, 'education/courses/discussion_reply.html', {
        'form': form,
        'discussion': discussion
    })


# Instructor views
class InstructorRequiredMixin(UserPassesTestMixin):
    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.is_staff


class CourseCreateView(InstructorRequiredMixin, CreateView):
    model = BiblicalCourse
    form_class = BiblicalCourseForm
    template_name = 'education/courses/course_form.html'
    success_url = reverse_lazy('education:course_list')


class CourseUpdateView(InstructorRequiredMixin, UpdateView):
    model = BiblicalCourse
    form_class = BiblicalCourseForm
    template_name = 'education/courses/course_form.html'
    success_url = reverse_lazy('education:course_list')


@login_required
def grade_assignment(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to grade assignments.')
        return redirect('education:course_list')

    if request.method == 'POST':
        form = AssignmentGradingForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.graded_by = request.user
            submission.graded_date = timezone.now()
            submission.save()
            messages.success(request, 'Assignment graded successfully!')
            return redirect('assignment_list')
    else:
        form = AssignmentGradingForm(instance=submission)

    return render(request, 'education/courses/grade_assignment.html', {
        'form': form,
        'submission': submission
    })
