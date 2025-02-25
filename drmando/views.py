from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .forms import CourseForm, ModuleForm, UserRegistrationForm
from .models import Course, Subject, Enrollment, Module


def home(request):
    featured_courses = Course.objects.filter(status='published')[:6]
    subjects = Subject.objects.all()
    return render(request, 'home.html', {
        'featured_courses': featured_courses,
        'subjects': subjects
    })


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

    def get_queryset(self):
        queryset = Course.objects.filter(status='published')
        subject_slug = self.kwargs.get('subject_slug')
        if subject_slug:
            subject = get_object_or_404(Subject, slug=subject_slug)
            queryset = queryset.filter(subject=subject)
        return queryset


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = Enrollment.objects.filter(
                student=self.request.user,
                course=self.object
            ).exists()
        return context


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    if created:
        messages.success(request, f'You have successfully enrolled in {course.title}')
    else:
        messages.info(request, f'You are already enrolled in {course.title}')
    return redirect('course_detail', slug=course.slug)


@login_required
def dashboard(request):
    enrolled_courses = Course.objects.filter(
        enrollments__student=request.user
    )
    return render(request, 'dashboard.html', {
        'enrolled_courses': enrolled_courses
    })


class SubjectListView(ListView):
    model = Subject
    template_name = 'courses/subject_list.html'
    context_object_name = 'subjects'
