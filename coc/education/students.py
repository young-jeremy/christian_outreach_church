from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from ...forms.bible_college import BibleCollegeStudentForm
from ...models.bible_college import (
    BibleCollegeStudent, BibleCollegeCourseEnrollment,
    BibleCollegeAssignment
)


@login_required
def student_dashboard(request):
    try:
        student = request.user.bible_college_student
        enrollments = BibleCollegeCourseEnrollment.objects.filter(
            student=student,
            completed=False
        )
        assignments = BibleCollegeAssignment.objects.filter(
            course__in=enrollments.values_list('course', flat=True)
        ).order_by('due_date')

        context = {
            'student': student,
            'enrollments': enrollments,
            'upcoming_assignments': assignments,
            'current_gpa': calculate_gpa(student)
        }
        return render(request, 'education/bible_college/student/dashboard.html', context)
    except BibleCollegeStudent.DoesNotExist:
        return redirect('education:student_registration')


@login_required
def student_registration(request):
    if hasattr(request.user, 'bible_college_student'):
        return redirect('education:student_dashboard')

    if request.method == 'POST':
        form = BibleCollegeStudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.enrollment_date = timezone.now().date()
            student.current_year = 1
            student.expected_graduation = calculate_graduation_date(
                student.enrollment_date,
                form.cleaned_data['program'].duration_years
            )
            student.save()
            messages.success(request, 'Successfully registered for Bible College!')
            return redirect('education:student_dashboard')
    else:
        form = BibleCollegeStudentForm()

    return render(request, 'education/bible_college/student/registration.html', {
        'form': form
    })


@login_required
def student_profile(request):
    student = get_object_or_404(BibleCollegeStudent, user=request.user)
    if request.method == 'POST':
        form = BibleCollegeStudentForm(
            request.POST,
            request.FILES,
            instance=student
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('education:student_dashboard')
    else:
        form = BibleCollegeStudentForm(instance=student)

    return render(request, 'education/bible_college/student/profile.html', {
        'form': form,
        'student': student
    })


def calculate_gpa(student):
    completed_enrollments = BibleCollegeCourseEnrollment.objects.filter(
        student=student,
        completed=True
    )
    if not completed_enrollments.exists():
        return 0.0

    total_points = 0
    total_credits = 0

    grade_points = {
        'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0
    }

    for enrollment in completed_enrollments:
        if enrollment.grade in grade_points:
            credits = enrollment.course.credits
            total_points += grade_points[enrollment.grade] * credits
            total_credits += credits

    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0


def calculate_graduation_date(enrollment_date, duration_years):
    from dateutil.relativedelta import relativedelta
    return enrollment_date + relativedelta(years=duration_years)
