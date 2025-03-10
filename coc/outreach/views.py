from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

from .models import *
from .forms import *

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Mission, Project, ProjectUpdate
from .forms import MissionForm, ProjectForm, ProjectUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Mission, Project, ProjectUpdate
from .forms import MissionForm, ProjectForm, ProjectUpdateForm
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Mission
from .forms import MissionForm

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Mission, Project, ProjectUpdate
from .forms import MissionForm, ProjectForm, ProjectUpdateForm
# Add to your existing views.py
from django.http import FileResponse
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import (PrisonFacility, InmateProgram, PrisonVisit,
                     VolunteerApplication, MinistryResource, )
from .forms import (VolunteerApplicationForm, PrisonVisitForm,
                    ResourceRequestForm)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from .models import (Hospital, Department, MinistryService, VisitSchedule,
                     PatientRequest, HospitalVisitReport, PrisonVisitReport, HospitalVolunteer)
from .forms import (HospitalVolunteerForm, VisitScheduleForm, PatientRequestForm,
                    HospitalVisitReportForm, PrisonVisitReportForm)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import VisitSchedule, PatientRequest
from .forms import VisitScheduleForm


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = 'outreach/hospital/visit_form.html'
    success_url = reverse_lazy('outreach:dashboard')

    def form_valid(self, form):
        visit = form.save(commit=False)
        visit.status = 'scheduled'
        visit.save()
        # Add the current user as a volunteer
        visit.volunteers.add(self.request.user)
        form.save_m2m()  # Save the many-to-many relationships
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule New Visit'
        context['submit_text'] = 'Schedule Visit'
        return context


class VisitUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = 'outreach/hospital/visit_form.html'
    success_url = reverse_lazy('outreach:dashboard')

    def get_queryset(self):
        # Only allow editing visits where the user is a volunteer
        return VisitSchedule.objects.filter(volunteers=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Visit'
        context['submit_text'] = 'Update Visit'
        return context


class PatientRequestDetailView(LoginRequiredMixin, DetailView):
    model = PatientRequest
    template_name = 'outreach/hospital/patient_request_detail.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_request = self.get_object()

        # Add related visits
        context['related_visits'] = VisitSchedule.objects.filter(
            department=patient_request.department,
            status='scheduled'
        ).order_by('date')[:5]

        # Add available volunteers
        context['available_volunteers'] = HospitalVolunteer.objects.filter(
            status='approved',
            hospitals=patient_request.department.hospital
        )

        # Check if current user can handle this request
        context['can_handle_request'] = (
                self.request.user.is_staff or
                hasattr(self.request.user, 'hospitalvolunteer') and
                self.request.user.hospitalvolunteer.status == 'approved' and
                self.request.user.hospitalvolunteer.hospitals.filter(
                    id=patient_request.department.hospital.id
                ).exists()
        )

        return context


class HospitalListView(ListView):
    model = Hospital
    template_name = 'outreach/hospital/hospital_list.html'
    context_object_name = 'hospitals'

    def get_queryset(self):
        return Hospital.objects.filter(active=True)


class HospitalDetailView(DetailView):
    model = Hospital
    template_name = 'outreach/hospital/hospital_detail.html'
    context_object_name = 'hospital'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = self.object.department_set.all()
        context['services'] = MinistryService.objects.filter(departments__hospital=self.object).distinct()
        context['upcoming_visits'] = self.object.visitschedule_set.filter(
            status='scheduled',
            date__gte=timezone.now()
        ).order_by('date')[:5]
        return context


@login_required
def volunteer_registration(request):
    try:
        volunteer = request.user.hospitalvolunteer
        form = HospitalVolunteerForm(instance=volunteer)
    except HospitalVolunteer.DoesNotExist:
        form = HospitalVolunteerForm()

    if request.method == 'POST':
        if hasattr(request.user, 'hospitalvolunteer'):
            form = HospitalVolunteerForm(request.POST, instance=request.user.hospitalvolunteer)
        else:
            form = HospitalVolunteerForm(request.POST)

        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.user = request.user
            volunteer.save()
            form.save_m2m()
            messages.success(request, 'Volunteer profile updated successfully!')
            return redirect('outreach:dashboard')

    return render(request, 'outreach/hospital/volunteer_registration.html', {'form': form})


@login_required
def hospital_ministry_dashboard(request):
    try:
        volunteer = request.user.hospitalvolunteer
        upcoming_visits = VisitSchedule.objects.filter(
            volunteers=request.user,
            status='scheduled',
            date__gte=timezone.now()
        ).order_by('date')

        assigned_requests = PatientRequest.objects.filter(
            assigned_to=request.user,
            status='assigned'
        ).order_by('priority', 'created_at')

        completed_visits = VisitSchedule.objects.filter(
            volunteers=request.user,
            status='completed'
        ).order_by('-date')[:5]

    except HospitalVolunteer.DoesNotExist:
        volunteer = None
        upcoming_visits = []
        assigned_requests = []
        completed_visits = []

    return render(request, 'outreach/hospital/dashboard.html', {
        'volunteer': volunteer,
        'upcoming_visits': upcoming_visits,
        'assigned_requests': assigned_requests,
        'completed_visits': completed_visits
    })


@login_required
def submit_visit_report(request, visit_id):
    visit = get_object_or_404(VisitSchedule, id=visit_id, volunteers=request.user)

    if request.method == 'POST':
        form = HospitalVisitReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.visit = visit
            report.submitted_by = request.user
            report.save()

            visit.status = 'completed'
            visit.save()

            messages.success(request, 'Visit report submitted successfully!')
            return redirect('outreach:hospital_ministry_dashboard')
    else:
        form = HospitalVisitReportForm()

    return render(request, 'outreach/hospital/submit_report.html', {
        'form': form,
        'visit': visit
    })


@login_required
def patient_request_form(request):
    if request.method == 'POST':
        form = PatientRequestForm(request.POST)
        if form.is_valid():
            patient_request = form.save()
            messages.success(request, 'Patient request submitted successfully!')
            return redirect('outreach:dashboard')
    else:
        form = PatientRequestForm()

    return render(request, 'outreach/hospital/patient_request_form.html', {'form': form})


class FacilityListView(ListView):
    model = PrisonFacility
    template_name = 'outreach/prison/facility_list.html'
    context_object_name = 'facilities'

    def get_queryset(self):
        return PrisonFacility.objects.filter(active=True)


class FacilityDetailView(DetailView):
    model = PrisonFacility
    template_name = 'outreach/prison/facility_detail.html'
    context_object_name = 'facility'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = self.object.inmateprogram_set.filter(active=True)
        context['upcoming_visits'] = self.object.prisonvisit_set.filter(
            status='scheduled'
        ).order_by('date')[:5]
        return context


@login_required
def volunteer_application(request, facility_id):
    facility = get_object_or_404(PrisonFacility, id=facility_id)

    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.facility = facility
            application.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Application submitted successfully!')
            return redirect('outreach:facility_detail', pk=facility_id)
    else:
        form = VolunteerApplicationForm()

    return render(request, 'outreach/prison/volunteer_application.html', {
        'form': form,
        'facility': facility
    })


@login_required
def prison_ministry_dashboard(request):
    user_applications = VolunteerApplication.objects.filter(user=request.user)
    upcoming_visits = PrisonVisit.objects.filter(
        volunteers=request.user,
        status='scheduled'
    ).order_by('date')
    completed_visits = PrisonVisit.objects.filter(
        volunteers=request.user,
        status='completed'
    ).order_by('-date')[:5]

    return render(request, 'outreach/prison/dashboard.html', {
        'applications': user_applications,
        'upcoming_visits': upcoming_visits,
        'completed_visits': completed_visits
    })


@login_required
def submit_visit_report(request, visit_id):
    visit = get_object_or_404(PrisonVisit, id=visit_id)

    if request.method == 'POST':
        form = PrisonVisitReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.visit = visit
            report.submitted_by = request.user
            report.save()
            form.save_m2m()
            messages.success(request, 'Visit report submitted successfully!')
            return redirect('outreach:prison_ministry_dashboard')
    else:
        form = PrisonVisitReportForm()

    return render(request, 'outreach/prison/submit_report.html', {
        'form': form,
        'visit': visit
    })


class TrackListView(ListView):
    model = DiscipleshipTrack
    template_name = 'outreach/discipleship/track_list.html'
    context_object_name = 'tracks'

    def get_queryset(self):
        return DiscipleshipTrack.objects.filter(is_active=True)


class TrackDetailView(DetailView):
    model = DiscipleshipTrack
    template_name = 'outreach/discipleship/track_detail.html'
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = MentorshipRelationship.objects.filter(
                mentee=self.request.user,
                track=self.object,
                status='active'
            ).exists()
            context['available_mentors'] = self.object.mentorshiprelationship_set.filter(
                status='active'
            ).values('mentor').annotate(
                mentee_count=Count('mentee')
            ).filter(mentee_count__lt=3)  # Limiting to mentors with less than 3 mentees
        return context


@login_required
def lesson_detail(request, track_slug, module_id, lesson_id):
    lesson = get_object_or_404(DiscipleshipLesson,
                               id=lesson_id,
                               module__id=module_id,
                               module__track__slug=track_slug)

    progress, created = DiscipleshipProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    if request.method == 'POST':
        form = LessonReflectionForm(request.POST, instance=progress)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.completed = True
            progress.completion_date = timezone.now()
            progress.save()
            messages.success(request, 'Reflection submitted successfully!')
            return redirect('outreach:module_detail', track_slug=track_slug, module_id=module_id)
    else:
        form = LessonReflectionForm(instance=progress)

    return render(request, 'outreach/discipleship/lesson_detail.html', {
        'lesson': lesson,
        'progress': progress,
        'form': form
    })


@login_required
def request_mentor(request, track_slug):
    track = get_object_or_404(DiscipleshipTrack, slug=track_slug)

    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            relationship = form.save(commit=False)
            relationship.mentee = request.user
            relationship.track = track
            relationship.start_date = timezone.now().date()
            relationship.save()
            messages.success(request, 'Mentorship request submitted successfully!')
            return redirect('outreach:track_detail', slug=track_slug)
    else:
        form = MentorshipRequestForm()

    return render(request, 'outreach/discipleship/request_mentor.html', {
        'track': track,
        'form': form
    })


@login_required
def mentorship_dashboard(request):
    # For mentees
    my_mentorships = MentorshipRelationship.objects.filter(
        mentee=request.user,
        status='active'
    )

    # For mentors
    my_mentees = MentorshipRelationship.objects.filter(
        mentor=request.user,
        status='active'
    )

    upcoming_meetings = MentorshipMeeting.objects.filter(
        Q(relationship__mentor=request.user) | Q(relationship__mentee=request.user),
        date__gte=timezone.now()
    ).order_by('date')

    return render(request, 'outreach/discipleship/mentorship_dashboard.html', {
        'my_mentorships': my_mentorships,
        'my_mentees': my_mentees,
        'upcoming_meetings': upcoming_meetings
    })


@login_required
def schedule_meeting(request, relationship_id):
    relationship = get_object_or_404(MentorshipRelationship, id=relationship_id)

    if request.user not in [relationship.mentor, relationship.mentee]:
        messages.error(request, 'You are not authorized to schedule this meeting.')
        return redirect('outreach:mentorship_dashboard')

    if request.method == 'POST':
        form = MentorshipMeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.relationship = relationship
            meeting.save()
            messages.success(request, 'Meeting scheduled successfully!')
            return redirect('outreach:mentorship_dashboard')
    else:
        form = MentorshipMeetingForm()

    return render(request, 'outreach/discipleship/schedule_meeting.html', {
        'relationship': relationship,
        'form': form
    })


# Add these views to your existing views.py

class CharityCampaignListView(ListView):
    model = CharityCampaign
    template_name = 'outreach/charity/campaign_list.html'
    context_object_name = 'campaigns'
    paginate_by = 9

    def get_queryset(self):
        queryset = CharityCampaign.objects.filter(status='active')
        cause = self.request.GET.get('cause')
        if cause:
            queryset = queryset.filter(cause=cause)
        return queryset


class CharityCampaignDetailView(DetailView):
    model = CharityCampaign
    template_name = 'outreach/charity/campaign_detail.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donation_form'] = DonationForm()
        context['recent_donations'] = self.object.donations.filter(
            payment_status='completed'
        ).order_by('-created_at')[:5]
        context['upcoming_events'] = self.object.events.filter(
            date__gte=timezone.now()
        ).order_by('date')
        return context


@login_required
def make_donation(request, campaign_slug):
    campaign = get_object_or_404(CharityCampaign, slug=campaign_slug)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.campaign = campaign
            donation.donor = request.user
            donation.payment_status = 'pending'
            donation.save()

            # Here you would integrate with a payment gateway
            # For now, we'll just mark it as completed
            donation.payment_status = 'completed'
            donation.save()

            campaign.raised_amount += donation.amount
            campaign.save()

            messages.success(request, 'Thank you for your donation!')
            return redirect('outreach:campaign_detail', slug=campaign_slug)
    return redirect('outreach:campaign_detail', slug=campaign_slug)


@login_required
def charity_dashboard(request):
    user_donations = Donation.objects.filter(
        donor=request.user,
        payment_status='completed'
    )
    total_donated = user_donations.aggregate(Sum('amount'))['amount__sum'] or 0
    upcoming_events = EventRegistration.objects.filter(
        participant=request.user,
        event__date__gte=timezone.now()
    ).select_related('event')

    return render(request, 'outreach/charity/dashboard.html', {
        'total_donated': total_donated,
        'recent_donations': user_donations.order_by('-created_at')[:5],
        'upcoming_events': upcoming_events,
    })


@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(CharityEvent, id=event_id)
    if event.current_participants >= event.max_participants:
        messages.error(request, 'Sorry, this event is full.')
        return redirect('outreach:campaign_detail', slug=event.campaign.slug)

    registration, created = EventRegistration.objects.get_or_create(
        event=event,
        participant=request.user
    )

    if created:
        event.current_participants += 1
        event.save()
        messages.success(request, 'You have successfully registered for the event!')
    else:
        messages.info(request, 'You are already registered for this event.')

    return redirect('outreach:campaign_detail', slug=event.campaign.slug)


class ServiceProjectListView(ListView):
    model = ServiceProject
    template_name = 'outreach/service/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        queryset = ServiceProject.objects.all()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        return context


class ServiceProjectDetailView(DetailView):
    model = ServiceProject
    template_name = 'outreach/service/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_hours'] = ServiceHours.objects.filter(
                student=self.request.user,
                project=self.object
            )
        return context


@login_required
def log_service_hours(request, project_slug):
    project = get_object_or_404(ServiceProject, slug=project_slug)
    if request.method == 'POST':
        form = ServiceHoursForm(request.POST)
        if form.is_valid():
            hours = form.save(commit=False)
            hours.student = request.user
            hours.project = project
            hours.save()
            messages.success(request, 'Service hours logged successfully!')
            return redirect('outreach:service_project_detail', slug=project_slug)
    else:
        form = ServiceHoursForm(initial={'project': project})
    return render(request, 'outreach/service/log_hours.html', {'form': form, 'project': project})


@login_required
def submit_reflection(request, project_slug):
    project = get_object_or_404(ServiceProject, slug=project_slug)
    if request.method == 'POST':
        form = ServiceReflectionForm(request.POST, request.FILES)
        if form.is_valid():
            reflection = form.save(commit=False)
            reflection.student = request.user
            reflection.project = project
            reflection.save()
            messages.success(request, 'Reflection submitted successfully!')
            return redirect('outreach:service_project_detail', slug=project_slug)
    else:
        form = ServiceReflectionForm()
    return render(request, 'outreach/service/submit_reflection.html', {'form': form, 'project': project})


@login_required
def service_dashboard(request):
    user_hours = ServiceHours.objects.filter(student=request.user)
    total_hours = user_hours.aggregate(Sum('hours'))['hours__sum'] or 0
    recent_projects = ServiceProject.objects.filter(
        volunteer_hours__student=request.user
    ).distinct()[:5]

    return render(request, 'outreach/service/dashboard.html', {
        'total_hours': total_hours,
        'recent_projects': recent_projects,
        'user_hours': user_hours[:5]
    })



class ToolListView(ListView):
    model = EvangelismTool
    template_name = 'outreach/evangelism_tools/tool_list.html'
    context_object_name = 'tools'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(EvangelismTool.CATEGORY_CHOICES)
        context['featured_tools'] = EvangelismTool.objects.filter(is_featured=True)[:4]
        return context

    def get_queryset(self):
        queryset = EvangelismTool.objects.all()
        category = self.request.GET.get('category')
        language = self.request.GET.get('language')
        search = self.request.GET.get('search')

        if category:
            queryset = queryset.filter(category=category)
        if language:
            queryset = queryset.filter(language=language)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__icontains=search)
            )
        return queryset


class ToolDetailView(DetailView):
    model = EvangelismTool
    template_name = 'outreach/evangelism_tools/tool_detail.html'
    context_object_name = 'tool'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tools'] = EvangelismTool.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context


class ToolCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EvangelismTool
    template_name = 'outreach/evangelism_tools/tool_form.html'
    fields = ['title', 'description', 'category', 'language', 'file',
              'external_link', 'thumbnail', 'author', 'publisher',
              'publication_date', 'is_featured']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, f'Tool "{form.instance.title}" has been created successfully.')
        return super().form_valid(form)


class ToolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EvangelismTool
    template_name = 'outreach/evangelism_tools/tool_form.html'
    fields = ['title', 'description', 'category', 'language', 'file',
              'external_link', 'thumbnail', 'author', 'publisher',
              'publication_date', 'is_featured']

    def test_func(self):
        return self.request.user.is_staff


def download_tool(request, slug):
    tool = get_object_or_404(EvangelismTool, slug=slug)
    if tool.file:
        tool.download_count = F('download_count') + 1
        tool.save()
        return FileResponse(tool.file.open(), as_attachment=True)
    return redirect(tool.external_link)


class MissionListView(ListView):
    model = Mission
    template_name = 'outreach/missions/mission_list.html'
    context_object_name = 'missions'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_missions'] = Mission.objects.filter(status='active')
        context['planned_missions'] = Mission.objects.filter(status='planned')
        return context


class MissionDetailView(DetailView):
    model = Mission
    template_name = 'outreach/missions/mission_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.all()
        return context


class MissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mission
    form_class = MissionForm
    template_name = 'outreach/missions/mission_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Mission'
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Mission "{form.instance.title}" has been created successfully.')
        return super().form_valid(form)


class MissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'outreach/missions/mission_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Mission: {self.object.title}'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Mission "{form.instance.title}" has been updated successfully.')
        return super().form_valid(form)


class MissionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mission
    template_name = 'outreach/missions/mission_confirm_delete.html'
    success_url = reverse_lazy('outreach:mission_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        mission = self.get_object()
        messages.success(self.request, f'Mission "{mission.title}" has been deleted.')
        return super().delete(request, *args, **kwargs)


class MissionEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'outreach/missions/mission_form.html'

    def test_func(self):
        """Only allow staff members to edit missions"""
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Mission: {self.object.title}'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Mission "{form.instance.title}" has been updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('outreach:mission_detail', kwargs={'slug': self.object.slug})

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to edit missions.')
        return super().handle_no_permission()


class ProjectListView(ListView):
    model = Project
    template_name = 'outreach/missions/project_list.html'
    context_object_name = 'projects'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(Project.CATEGORY_CHOICES)
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'outreach/missions/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['updates'] = self.object.updates.all()
        return context


class ProjectUpdateCreateView(LoginRequiredMixin, CreateView):
    model = ProjectUpdate
    form_class = ProjectUpdateForm
    template_name = 'outreach/missions/project_update_form.html'

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('outreach:project_detail', kwargs={'slug': self.object.project.slug})


# Project Views
class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'outreach/missions/project_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        initial = super().get_initial()
        mission_id = self.request.GET.get('mission')
        if mission_id:
            initial['mission'] = get_object_or_404(Mission, id=mission_id)
        return initial


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'outreach/missions/project_form.html'

    def test_func(self):
        return self.request.user.is_staff


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'outreach/missions/project_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('outreach:mission_detail',
                            kwargs={'slug': self.object.mission.slug})


# Project Update Views
class ProjectUpdateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProjectUpdate
    form_class = ProjectUpdateForm
    template_name = 'outreach/missions/project_update_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('outreach:project_detail',
                            kwargs={'slug': self.object.project.slug})


class ProjectUpdateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProjectUpdate
    template_name = 'outreach/missions/project_update_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('outreach:project_detail',
                            kwargs={'slug': self.object.project.slug})
