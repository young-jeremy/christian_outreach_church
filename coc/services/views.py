from django.urls import reverse
# Settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    SinglesMinistry,
    SinglesEvent,
    MentorshipRequest,
    SinglesResource, SermonNote
)
from .forms import (
    SinglesMinistryForm,
    SinglesEventForm,
    MentorshipRequestForm,
    SinglesResourceForm,
    MentorshipMatchForm,
    SinglesEventRegistrationForm
)
from django.contrib.auth.models import User
from .models import (
    SeniorsMinistry,
    SeniorsEvent,
    TransportationRequest,
    HealthResource,
    PrayerPartner
)
from .forms import (
    SeniorsMinistryForm,
    SeniorsEventForm,
    TransportationRequestForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import SeniorsMinistry, SeniorsEvent, TransportationRequest
from .forms import SeniorsMinistryForm, TransportationRequestForm, SeniorsEventForm
from .models import MensMinistry, MensEvent
from .forms import MensMinistryForm, MensEventForm
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import YouthProgram, YouthEvent
from .forms import YouthProgramForm, YouthEventForm
from django.db import models
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .models import (
    YouthProgram,
    YouthEvent,
    YouthEventAttendee,
    YouthEventPayment,  # Changed from Payment
    PermissionSlip,
    AttendanceRecord
)
from .forms import YouthProgramForm, YouthEventForm, PaymentForm, PermissionSlipForm
from django.utils import timezone

# Rest of the code remains the same...from .forms import YouthProgramForm, YouthEventForm, PaymentForm, PermissionSlipForm
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from videos.models import Comments
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import CreateView, DeleteView
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic import (
    TemplateView
)

from accounts.forms import UserForm, MemberProfileForm
from accounts.models import MemberProfile
from videos.models import Content
from .forms import BibleStudyForm
from .forms import (
    FamilyEventForm, ParentingResourceForm,
    FamilyCounselingForm, FamilyDiscussionForm, DiscussionCommentForm
)
from .forms import (
    MarriageMinistryForm, CoupleProfileForm, MarriageCounselingForm
)
from .forms import (
    NewBelieverProfileForm, MentorshipSessionForm, PrayerJournalForm, BibleReadingPlanForm
)
from .forms import PostForm
from .forms import SermonCategoryForm
from .forms import TopicForm
from .forms import VolunteerOpportunityForm, VolunteerSignupForm
from .forms import WorshipServiceForm
# Local forms
from .forms import (
    # Import all your forms here...
    YouthEventForm,
    ChildrenProgramForm, ChildRegistrationForm,
    CounselingSessionForm, JournalEntryForm,
    SongRequestForm,
    TestimonyForm, SermonForm, PrayerRequestForm, SmallGroupForm, CounselingRequestForm
)
# Local integrations
from .integrations import (
    CalendarIntegration, VideoConference,
    NotificationService, AIAssistant, CoupleAnalytics
)
from .models import BibleStudy
from .models import Channel, Subscription
# Local models
from .models import (
    # Core models
    Event, EventRegistration, Ministry,

    # Bible Study related
    BibleReading, BelieverProgress,
    # Service related
    # Youth and Children
    YouthEvent, ChildrenProgram,
    # Groups and Registration
    SmallGroup,  # Couples Ministry
    CoupleEvent, CounselingSession,
    CoupleResource, CoupleJournal, DateNightIdea,
    CouplePrayerRequest,

    # Prayer and Notifications
    PrayerRequest,  # Forums
    # New Believers
    ReadingProgress,

    # Testimonies
    Testimony
)
from .models import (
    FamilyEvent, ParentingResource,
    FamilyCounseling, FamilyDiscussion
)
from .models import ForumCategory, Topic, Post
from .models import (
    MarriageMinistry, CoupleProfile, MarriageResource, MarriageCounseling, MarriageEvent
)
from .models import (
    NewBelieverProfile, DiscipleshipTrack, DiscipleshipModule,
    MentorshipSession, PrayerJournal, BibleReadingPlan
)
from .models import Sermon, SermonCategory, SermonNote
from .models import VolunteerOpportunity, VolunteerSignup
from .models import WorshipService
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WomensMinistry, MinistryEvent
from .forms import WomensMinistryForm, MinistryEventForm


class SermonResourcesView(ListView):
    template_name = 'services/sermons/sermon_resources.html'
    context_object_name = 'sermon_resources'
    paginate_by = 12

    def get_queryset(self):
        # Get only sermons that have either audio recordings or slides
        return SermonNote.objects.filter(
            Q(audio_recording__isnull=False) | Q(presentation_file__isnull=False)
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(SermonNote.CATEGORY_CHOICES)
        return context


def add_sermon_view(request):
    if request.method == 'POST':
        # ... your form processing code ...
        if form.is_valid():
            sermon = form.save()
            # Use the correct URL name
            return redirect('videos:sermon_details', video_id=sermon.id)
    # ... rest of your view code ...


def womens_ministry_list(request):
    ministries = WomensMinistry.objects.filter(is_active=True)
    context = {
        'ministries': ministries,
    }
    return render(request, 'services/womens_ministry/list.html', context)


def womens_ministry_detail(request, slug):
    ministry = get_object_or_404(WomensMinistry, slug=slug)
    events = ministry.events.all().order_by('date')
    context = {
        'ministry': ministry,
        'events': events,
    }
    return render(request, 'services/womens_ministry/detail.html', context)


@login_required
def womens_ministry_create(request):
    if request.method == 'POST':
        form = WomensMinistryForm(request.POST, request.FILES)
        if form.is_valid():
            ministry = form.save(commit=False)
            ministry.leader = request.user
            ministry.save()
            messages.success(request, 'Ministry created successfully!')
            return redirect('videos:womens_ministry_detail', slug=ministry.slug)
    else:
        form = WomensMinistryForm()

    return render(request, 'services/womens_ministry/form.html', {'form': form, 'action': 'Create'})


@login_required
def ministry_event_create(request, ministry_slug):
    ministry = get_object_or_404(WomensMinistry, slug=ministry_slug)
    if request.method == 'POST':
        form = MinistryEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.ministry = ministry
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('videos:womens_ministry_detail', slug=ministry.slug)
    else:
        form = MinistryEventForm()

    return render(request, 'services/womens_ministry/event_form.html', {
        'form': form,
        'ministry': ministry,
        'action': 'Create'
    })


@login_required
def create_worship_service(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create worship services.')
        return redirect('services:worship_service_list')

    if request.method == 'POST':
        form = WorshipServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Worship service created successfully!')
            return redirect('services:worship_service_list')
    else:
        form = WorshipServiceForm()

    context = {
        'form': form,
        'title': 'Create Worship Service'
    }

    return render(request, 'services/create_worship_service.html', context)



@login_required
def video_feed(request):
    subscriptions = Subscription.objects.filter(subscriber=request.user)
    channels = [subscription.channel for subscription in subscriptions]
    videos = Content.objects.filter(channel__in=channels).order_by('-uploaded_at')
    return render(request, 'video_feed.html', {'videos': videos})


@login_required
def subscriptions_view(request):
    """View for managing subscriptions"""
    subscriptions = Subscription.objects.filter(subscriber=request.user)
    available_channels = Channel.objects.exclude(
        subscribers__subscriber=request.user
    )
    return render(request, 'services/subscriptions.html', {
        'subscriptions': subscriptions,
        'available_channels': available_channels
    })


@login_required
def subscribe_view(request, channel_id):
    """Handle channel subscription"""
    channel = get_object_or_404(Channel, id=channel_id)
    subscription, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        channel=channel
    )
    if created:
        messages.success(request, f'Successfully subscribed to {channel.name}')
    return redirect('services:subscriptions')


@login_required
def unsubscribe_view(request, channel_id):
    """Handle channel unsubscription"""
    subscription = get_object_or_404(
        Subscription, 
        subscriber=request.user, 
        channel_id=channel_id
    )
    subscription.delete()
    messages.success(request, 'Successfully unsubscribed')
    return redirect('services:subscriptions')


@login_required
def services(request):
    """Home view for services section"""
    context = {
        'recent_sermons': Sermon.objects.all().order_by('-date_preached')[:3],
        'upcoming_events': Event.objects.filter(
            start_date__gte=timezone.now()
        ).order_by('start_date')[:5],
        'bible_studies': BibleStudy.objects.filter(
            start_date__gte=timezone.now()
        ).order_by('start_date')[:3]
    }
    return render(request, 'services/home.html', context)


class MemberDirectoryView(LoginRequiredMixin, ListView):
    model = MemberProfile
    template_name = 'members/directory.html'
    context_object_name = 'members'
    paginate_by = 12

    def get_queryset(self):
        queryset = MemberProfile.objects.filter(is_public=True)

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(skills__name__icontains=search_query) |
                Q(ministries__name__icontains=search_query)
            ).distinct()

        # Filter by ministry
        ministry = self.request.GET.get('ministry')
        if ministry:
            queryset = queryset.filter(ministries__name=ministry)

        return queryset.order_by('user__first_name', 'user__last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ministries'] = Ministry.objects.all()
        context['current_ministry'] = self.request.GET.get('ministry', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class MemberProfileView(LoginRequiredMixin, DetailView):
    model = MemberProfile
    template_name = 'members/profile.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = MemberProfile
    template_name = 'members/edit_profile.html'
    form_class = MemberProfileForm

    def get_object(self):
        return get_object_or_404(MemberProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        if user_form.is_valid():
            user_form.save()
            form.save()
            messages.success(self.request, 'Profile updated successfully!')
            return redirect('members:profile', slug=self.object.slug)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class BibleStudyListView(ListView):
    model = BibleStudy
    template_name = 'services/bible_study_list.html'
    context_object_name = 'bible_studies'
    paginate_by = 9

    def get_queryset(self):
        queryset = BibleStudy.objects.filter(is_active=True)

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(teacher__first_name__icontains=search_query) |
                Q(teacher__last_name__icontains=search_query)
            )

        # Filter by study type
        study_type = self.request.GET.get('type')
        if study_type:
            queryset = queryset.filter(study_type=study_type)

        return queryset.order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['study_types'] = BibleStudy.STUDY_TYPES
        context['current_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class BibleStudyDetailView(DetailView):
    model = BibleStudy
    template_name = 'services/bible_study_detail.html'
    context_object_name = 'study'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_participant'] = self.object.participants.filter(
                id=self.request.user.id
            ).exists()
            context['can_access_materials'] = (
                    context['is_participant'] or
                    self.request.user == self.object.teacher or
                    self.request.user.is_staff
            )
        return context


class BibleStudyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BibleStudy
    form_class = BibleStudyForm
    template_name = 'services/bible_study_form.html'
    success_url = reverse_lazy('services:bible_study_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'Bible Study created successfully!')
        return super().form_valid(form)


class BibleStudyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BibleStudy
    form_class = BibleStudyForm
    template_name = 'services/bible_study_form.html'

    def test_func(self):
        study = self.get_object()
        return self.request.user == study.teacher or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('services:bible_study_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Bible Study updated successfully!')
        return super().form_valid(form)


class BibleStudyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BibleStudy
    success_url = reverse_lazy('services:bible_study_list')
    template_name = 'services/bible_study_confirm_delete.html'

    def test_func(self):
        study = self.get_object()
        return self.request.user == study.teacher or self.request.user.is_staff


def join_bible_study(request, slug):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to join Bible Studies.')
        return redirect('login')

    study = get_object_or_404(BibleStudy, slug=slug, is_active=True)

    if study.max_participants and study.participants.count() >= study.max_participants:
        messages.warning(request, 'This Bible Study is already full.')
        return redirect('services:bible_study_detail', slug=slug)

    if study.participants.filter(id=request.user.id).exists():
        messages.info(request, 'You are already registered for this Bible Study.')
    else:
        study.participants.add(request.user)
        messages.success(request, 'You have successfully joined the Bible Study!')

        # Send confirmation email
        send_study_confirmation_email.delay(
            study.id,
            request.user.id
        )

    return redirect('services:bible_study_detail', slug=slug)


def leave_bible_study(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    study = get_object_or_404(BibleStudy, slug=slug)

    if study.participants.filter(id=request.user.id).exists():
        study.participants.remove(request.user)
        messages.success(request, 'You have left the Bible Study.')
    else:
        messages.info(request, 'You are not registered for this Bible Study.')

    return redirect('services:bible_study_detail', slug=slug)


def download_study_material(request, slug, filename):
    study = get_object_or_404(BibleStudy, slug=slug)

    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to access study materials.')
        return redirect('login')

    if not (study.participants.filter(id=request.user.id).exists() or
            request.user == study.teacher or
            request.user.is_staff):
        messages.warning(request, 'You must be registered for this study to access materials.')
        return redirect('services:bible_study_detail', slug=slug)

    try:
        response = FileResponse(study.materials)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except:
        messages.error(request, 'Error downloading the file.')
        return redirect('services:bible_study_detail', slug=slug)


@login_required
def family_discussion_like(request, slug):
    discussion = get_object_or_404(FamilyDiscussion, slug=slug)
    if request.user in discussion.likes.all():
        discussion.likes.remove(request.user)
    else:
        discussion.likes.add(request.user)
    return JsonResponse({
        'likes_count': discussion.likes.count(),
        'is_liked': request.user in discussion.likes.all()
    })

@login_required
def family_discussion_comment(request, slug):
    discussion = get_object_or_404(FamilyDiscussion, slug=slug)
    if request.method == 'POST':
        form = DiscussionCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Error adding comment.')
    return redirect('services:family_discussion_detail', slug=slug)


class ForumListView(ListView):
    model = ForumCategory
    template_name = 'services/forums/forum_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            category.topic_count = Topic.objects.filter(category=category).count()
            category.post_count = Post.objects.filter(topic__category=category).count()
            category.latest_topic = Topic.objects.filter(category=category).order_by('-created_at').first()
        return context

class ForumCategoryView(ListView):
    model = Topic
    template_name = 'services/forums/category.html'
    context_object_name = 'topics'
    paginate_by = 20

    def get_queryset(self):
        self.category = get_object_or_404(ForumCategory, slug=self.kwargs['category_slug'])
        return Topic.objects.filter(category=self.category).order_by('-is_pinned', '-last_activity')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ForumTopicView(DetailView):
    model = Topic
    template_name = 'services/forums/topic.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().select_related('author')
        context['form'] = PostForm()
        return context

class CreateForumTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'services/forums/create_topic.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


def health_check(request):
    # Remove Redis check if not needed
    return JsonResponse({
        'status': 'ok'
    })




class MemberListView(LoginRequiredMixin, ListView):
    model = MemberProfile
    template_name = 'members/member_list.html'
    context_object_name = 'members'
    paginate_by = 20

    def get_queryset(self):
        queryset = MemberProfile.objects.filter(user__is_active=True)
        return queryset.order_by('user__first_name', 'user__last_name')



class OpportunityListView(ListView):
    model = VolunteerOpportunity
    template_name = 'volunteers/opportunity_list.html'
    context_object_name = 'opportunities'
    paginate_by = 12

    def get_queryset(self):
        queryset = VolunteerOpportunity.objects.exclude(status='closed')

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(ministry__name__icontains=search_query)
            )

        # Filter by ministry
        ministry = self.request.GET.get('ministry')
        if ministry:
            queryset = queryset.filter(ministry__name=ministry)

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ministries'] = Ministry.objects.all()
        context['statuses'] = dict(VolunteerOpportunity.STATUS_CHOICES)
        return context


class OpportunityDetailView(DetailView):
    model = VolunteerOpportunity
    template_name = 'volunteers/opportunity_detail.html'
    context_object_name = 'opportunity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_coordinator'] = self.object.coordinator == self.request.user
            context['has_signed_up'] = VolunteerSignup.objects.filter(
                volunteer=self.request.user,
                opportunity=self.object
            ).exists()
            if context['has_signed_up']:
                context['signup'] = VolunteerSignup.objects.get(
                    volunteer=self.request.user,
                    opportunity=self.object
                )
        return context


class OpportunityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VolunteerOpportunity
    form_class = VolunteerOpportunityForm
    template_name = 'volunteers/opportunity_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.coordinator = self.request.user
        messages.success(self.request, 'Volunteer opportunity created successfully!')
        return super().form_valid(form)


class OpportunityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VolunteerOpportunity
    form_class = VolunteerOpportunityForm
    template_name = 'volunteers/opportunity_form.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.coordinator or self.request.user.is_staff


class OpportunityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VolunteerOpportunity
    template_name = 'volunteers/opportunity_confirm_delete.html'
    success_url = reverse_lazy('volunteers:opportunity_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.coordinator or self.request.user.is_staff


def volunteer_signup(request, slug):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to sign up for volunteer opportunities.')
        return redirect('login')

    opportunity = get_object_or_404(VolunteerOpportunity, slug=slug)

    if opportunity.is_full:
        messages.warning(request, 'This volunteer opportunity is already full.')
        return redirect('volunteers:opportunity_detail', slug=slug)

    if VolunteerSignup.objects.filter(volunteer=request.user, opportunity=opportunity).exists():
        messages.info(request, 'You have already signed up for this opportunity.')
        return redirect('volunteers:opportunity_detail', slug=slug)

    if request.method == 'POST':
        form = VolunteerSignupForm(request.POST)
        if form.is_valid():
            signup = form.save(commit=False)
            signup.volunteer = request.user
            signup.opportunity = opportunity
            signup.save()
            messages.success(request, 'Thank you for signing up! We will contact you soon.')
            return redirect('volunteers:opportunity_detail', slug=slug)
    else:
        form = VolunteerSignupForm()

    return render(request, 'volunteers/signup_form.html', {
        'form': form,
        'opportunity': opportunity
    })


def cancel_signup(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    opportunity = get_object_or_404(VolunteerOpportunity, slug=slug)
    signup = get_object_or_404(VolunteerSignup,
                               volunteer=request.user,
                               opportunity=opportunity)

    signup.delete()
    messages.success(request, 'Your signup has been cancelled.')
    return redirect('volunteers:opportunity_detail', slug=slug)



class ForumHomeView(LoginRequiredMixin, ListView):
    model = ForumCategory
    template_name = 'forums/home.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_topics'] = Topic.objects.order_by('-created_at')[:5]
        return context


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'forums/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(ForumCategory, slug=self.kwargs['category_slug'])
        return Topic.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class TopicDetailView(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = 'forums/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('created_at')
        context['form'] = PostForm()
        return context

class CreateTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'services/forums/create_topic.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forums/create_post.html'

    def form_valid(self, form):
        topic = get_object_or_404(Topic, slug=self.kwargs['topic_slug'])
        form.instance.topic = topic
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('services:topic_detail', kwargs={'slug': self.kwargs['topic_slug']})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})


class MarriageMinistryListView(LoginRequiredMixin, ListView):
    model = MarriageMinistry
    template_name = 'services/marriage/program_list.html'
    context_object_name = 'programs'
    paginate_by = 9

    def get_queryset(self):
        return MarriageMinistry.objects.all().order_by('-start_date')

class MarriageMinistryDetailView(DetailView):
    model = MarriageMinistry
    template_name = 'services/marriage/program_detail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['can_enroll'] = True  # Add enrollment logic here
        return context

class MarriageMinistryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MarriageMinistry
    form_class = MarriageMinistryForm
    template_name = 'services/marriage/program_form.html'

    def test_func(self):
        return self.request.user.is_staff

@login_required
def create_couple_profile(request):
    # Check if user already has a profile
    if hasattr(request.user, 'couple_profile') and request.user.couple_profile:
        messages.warning(request, 'You already have a couple profile.')
        return redirect('services:couples_home')

    if request.method == 'POST':
        form = CoupleProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Your couple profile has been created successfully!')
                return redirect('services:couples_home')
            except Exception as e:
                messages.error(request, f'An error occurred while creating your profile: {str(e)}')
                print(f"Error creating profile: {e}")  # For debugging
        else:
            messages.error(request, 'Please correct the errors below.')
            print(f"Form errors: {form.errors}")  # For debugging
    else:
        form = CoupleProfileForm()

    return render(request, 'services/couples/create_profile.html', {
        'form': form,
    })

class MarriageResourceListView(ListView):
    model = MarriageResource
    template_name = 'services/marriage/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12

class MarriageCounselingCreateView(LoginRequiredMixin, CreateView):
    model = MarriageCounseling
    form_class = MarriageCounselingForm
    template_name = 'services/marriage/counseling_form.html'

    def form_valid(self, form):
        couple = get_object_or_404(CoupleProfile, user1=self.request.user)
        form.instance.couple = couple
        return super().form_valid(form)

class MarriageEventListView(ListView):
    model = MarriageEvent
    template_name = 'services/marriage/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return MarriageEvent.objects.filter(date__gte=timezone.now()).order_by('date')





class FamilyResourceCreateView(LoginRequiredMixin, CreateView):
    model = ParentingResource
    form_class = ParentingResourceForm
    template_name = 'services/family/resource_form.html'
    success_url = reverse_lazy('services:family_resources')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Resource created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_types'] = ParentingResource.RESOURCE_TYPES
        context['age_groups'] = ParentingResource.AGE_GROUPS
        return context



class FamilyEventCreateView(LoginRequiredMixin, CreateView):
    model = FamilyEvent
    form_class = FamilyEventForm
    template_name = 'services/family/event_form.html'
    success_url = reverse_lazy('services:family_events')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Family event created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = FamilyEvent.EVENT_TYPES
        return context

class ScheduleCounseling(LoginRequiredMixin, CreateView):
    model = CounselingSession
    form_class = CounselingSessionForm
    template_name = 'services/couples/schedule_counseling.html'
    
    def form_valid(self, form):
        session = form.save(commit=False)
        couple = get_object_or_404(CoupleProfile, partner1=self.request.user)
        session.couple = couple
        
        # Create calendar event
        calendar = CalendarIntegration(self.request.user.calendar_credentials)
        event = calendar.add_event(
            title=f"Counseling: {session.get_session_type_display()}",
            start_time=session.scheduled_time,
            end_time=session.scheduled_time + session.duration,
            description=session.notes,
            attendees=[couple.partner1.email, couple.partner2.email, session.counselor.email]
        )
        
        # Create video conference if virtual
        if session.session_type == 'virtual':
            zoom = VideoConference(settings.ZOOM_API_KEY, settings.ZOOM_API_SECRET)
            meeting = zoom.create_meeting(
                topic=f"Counseling Session - {couple}",
                start_time=session.scheduled_time,
                duration=session.duration.total_seconds() // 60
            )
            session.virtual_meeting_link = meeting['join_url']
        
        session.save()
        
        # Send notifications
        notifications = NotificationService()
        reminder_message = f"Your counseling session is scheduled for {session.scheduled_time.strftime('%B %d, %Y at %I:%M %p')}"
        notifications.send_reminder(couple.partner1.phone_number, reminder_message)
        notifications.send_reminder(couple.partner2.phone_number, reminder_message)
        
        return super().form_valid(form)

class CoupleJournalList(LoginRequiredMixin, ListView):
    model = CoupleJournal
    template_name = 'services/couples/journal_list.html'
    context_object_name = 'entries'
    
    def get_queryset(self):
        couple = get_object_or_404(CoupleProfile, partner_name=self.request.user)
        return CoupleJournal.objects.filter(couple=couple)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get AI-powered insights
        ai = AIAssistant(settings.OPENAI_API_KEY)
        context['insights'] = ai.analyze_journal(self.get_queryset())
        
        # Get relationship analytics
        analytics = CoupleAnalytics()
        couple = get_object_or_404(CoupleProfile, partner1=self.request.user)
        context['analytics'] = analytics.generate_health_report(couple)
        
        return context



class FamilyDiscussionCreateView(LoginRequiredMixin, CreateView):
    model = FamilyDiscussion
    form_class = FamilyDiscussionForm
    template_name = 'services/family/create_discussion.html'
    success_url = reverse_lazy('services:family_discussions')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def family_discussion_like(request, slug):
    discussion = get_object_or_404(FamilyDiscussion, slug=slug)
    if request.user in discussion.likes.all():
        discussion.likes.remove(request.user)
        liked = False
    else:
        discussion.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': discussion.likes.count()})

@login_required
def family_discussion_comment(request, slug):
    discussion = get_object_or_404(FamilyDiscussion, slug=slug)
    if request.method == 'POST':
        form = DiscussionCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('services:family_discussion_detail', slug=slug)

class NewBelieversDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'services/new_believers/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        believer = get_object_or_404(NewBelieverProfile, user=self.request.user)
        context['believer'] = believer
        context['upcoming_sessions'] = MentorshipSession.objects.filter(
            mentee=believer,
            scheduled_time__gte=timezone.now()
        ).order_by('scheduled_time')
        return context

class NewBelieverProfileCreate(LoginRequiredMixin, CreateView):
    model = NewBelieverProfile
    form_class = NewBelieverProfileForm
    template_name = 'services/new_believers/profile_form.html'
    success_url = reverse_lazy('services:new_believers_dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Profile created successfully!')
        return super().form_valid(form)

class DiscipleshipTrackList(LoginRequiredMixin, ListView):
    model = DiscipleshipTrack
    template_name = 'services/new_believers/track_list.html'
    context_object_name = 'tracks'

class DiscipleshipTrackDetail(LoginRequiredMixin, DetailView):
    model = DiscipleshipTrack
    template_name = 'services/new_believers/track_detail.html'
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        believer = get_object_or_404(NewBelieverProfile, user=self.request.user)
        context['progress'] = BelieverProgress.objects.filter(
            believer=believer,
            module__track=self.object
        )
        return context

class MentorshipSessionList(LoginRequiredMixin, ListView):
    model = MentorshipSession
    template_name = 'services/new_believers/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        believer = get_object_or_404(NewBelieverProfile, user=self.request.user)
        return MentorshipSession.objects.filter(mentee=believer)

class ScheduleMentorshipSession(LoginRequiredMixin, CreateView):
    model = MentorshipSession
    form_class = MentorshipSessionForm
    template_name = 'services/new_believers/schedule_session.html'
    success_url = reverse_lazy('services:mentorship_sessions')

    def form_valid(self, form):
        believer = get_object_or_404(NewBelieverProfile, user=self.request.user)
        form.instance.mentee = believer
        messages.success(self.request, 'Session scheduled successfully!')
        return super().form_valid(form)

class PrayerJournalList(LoginRequiredMixin, ListView):
    model = PrayerJournal
    template_name = 'services/new_believers/prayer_journal.html'
    context_object_name = 'prayers'

    def get_queryset(self):
        believer = get_object_or_404(NewBelieverProfile, user=self.request.user)
        return PrayerJournal.objects.filter(believer=believer)

class BibleReadingPlanList(LoginRequiredMixin, ListView):
    model = BibleReadingPlan
    template_name = 'services/new_believers/reading_plan_list.html'
    context_object_name = 'plans'

class NewBelieverProfileView(LoginRequiredMixin, DetailView):
    model = NewBelieverProfile
    template_name = 'services/new_believers/profile.html'
    context_object_name = 'believer'

    def get_object(self):
        return get_object_or_404(NewBelieverProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'mentorship_sessions': MentorshipSession.objects.filter(
                mentee=self.object,
                completed=False
            ).order_by('scheduled_time')[:5],
            'completed_tracks': BelieverProgress.objects.filter(
                believer=self.object,
                completed=True
            ).values('module__track').distinct().count(),
            'total_tracks': DiscipleshipTrack.objects.count(),
            'recent_prayers': PrayerJournal.objects.filter(
                believer=self.object
            ).order_by('-created_at')[:3]
        })
        return context

class BibleReadingPlanDetail(LoginRequiredMixin, DetailView):
    model = BibleReadingPlan
    template_name = 'services/new_believers/reading_plan_detail.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        believer = get_object_or_404(NewBelieverProfile, user=self.request.user)
        context['readings'] = BibleReading.objects.filter(plan=self.object)
        context['progress'] = ReadingProgress.objects.filter(
            believer=believer,
            reading__plan=self.object
        )
        return context

@login_required
def complete_reading(request, plan_slug, day_number):
    plan = get_object_or_404(BibleReadingPlan, slug=plan_slug)
    reading = get_object_or_404(BibleReading, plan=plan, day_number=day_number)
    believer = get_object_or_404(NewBelieverProfile, user=request.user)

    progress, created = ReadingProgress.objects.get_or_create(
        believer=believer,
        reading=reading
    )
    progress.completed = True
    progress.completion_date = timezone.now()
    progress.save()

    messages.success(request, 'Reading marked as completed!')
    return redirect('services:reading_plan_detail', slug=plan_slug)

@login_required
def add_prayer_entry(request):
    if request.method == 'POST':
        form = PrayerJournalForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            believer = get_object_or_404(NewBelieverProfile, user=request.user)
            entry.believer = believer
            entry.save()
            messages.success(request, 'Prayer journal entry added successfully!')
            return redirect('services:prayer_journal')
    else:
        form = PrayerJournalForm()
    
    return render(request, 'services/new_believers/add_prayer.html', {'form': form})

@login_required
def update_prayer_status(request, pk):
    entry = get_object_or_404(PrayerJournal, pk=pk, believer__user=request.user)
    
    if request.method == 'POST':
        entry.answered = True
        entry.answer_date = timezone.now().date()
        entry.answer_notes = request.POST.get('answer_notes', '')
        entry.save()
        messages.success(request, 'Prayer status updated!')
    
    return redirect('services:prayer_journal')

@login_required
def complete_module(request, track_slug, module_id):
    module = get_object_or_404(DiscipleshipModule, id=module_id)
    believer = get_object_or_404(NewBelieverProfile, user=request.user)
    
    progress, created = BelieverProgress.objects.get_or_create(
        believer=believer,
        module=module
    )
    progress.completed = True
    progress.completion_date = timezone.now()
    progress.save()
    
    messages.success(request, 'Module marked as completed!')
    return redirect('services:track_detail', slug=track_slug)

@login_required
def complete_mentorship_session(request, session_id):
    session = get_object_or_404(MentorshipSession, id=session_id)
    if request.user == session.mentor:
        session.completed = True
        session.save()
        messages.success(request, 'Session marked as completed!')
    return redirect('services:mentorship_sessions')

@login_required
def update_baptism_status(request):
    if request.method == 'POST':
        believer = get_object_or_404(NewBelieverProfile, user=request.user)
        believer.baptism_status = True
        believer.baptism_date = request.POST.get('baptism_date')
        believer.save()
        messages.success(request, 'Baptism status updated!')
    return redirect('services:believer_profile')

class FamilyLifeHomeView(LoginRequiredMixin, ListView):
    template_name = 'services/family/home.html'
    model = FamilyEvent
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_discussions'] = FamilyDiscussion.objects.order_by(
            '-created_at'
        )[:5]
        context['resources'] = ParentingResource.objects.order_by(
            '-created_at'
        )[:6]
        return context

class FamilyEventListView(ListView):
    model = FamilyEvent
    template_name = 'services/family/event_list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset

class ParentingResourceListView(ListView):
    model = ParentingResource
    template_name = 'services/family/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        age_group = self.request.GET.get('age_group')
        resource_type = self.request.GET.get('type')
        search = self.request.GET.get('search')

        if age_group:
            queryset = queryset.filter(age_group=age_group)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

class FamilyDiscussionListView(ListView):
    model = FamilyDiscussion
    template_name = 'services/family/discussion_list.html'
    context_object_name = 'discussions'
    paginate_by = 10

class FamilyDiscussionDetailView(DetailView):
    model = FamilyDiscussion
    template_name = 'services/family/discussion_detail.html'
    context_object_name = 'discussion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = DiscussionCommentForm()
        return context

class FamilyCounselingCreateView(LoginRequiredMixin, CreateView):
    model = FamilyCounseling
    form_class = FamilyCounselingForm
    template_name = 'services/family/counseling_form.html'
    success_url = reverse_lazy('services:family_home')

    def form_valid(self, form):
        form.instance.family = self.request.user
        return super().form_valid(form)

@login_required
def submit_song_request(request):
    """Handle song request submission"""
    if request.method == 'POST':
        form = SongRequestForm(request.POST)
        if form.is_valid():
            song_request = form.save(commit=False)
            song_request.requester = request.user
            song_request.save()
            messages.success(request, 'Song request submitted successfully!')
            return redirect('services:worship_service_list')
    else:
        form = SongRequestForm()
    return render(request, 'services/worship/submit_song_request.html', {'form': form})

@login_required
def sermon_list(request):
    # Change ordering from 'date' to 'date_preached'
    sermons = Sermon.objects.all().order_by('-date_preached')
    
    # Filter by search query if provided
    search_query = request.GET.get('search', '')
    if search_query:
        sermons = sermons.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(scripture_reference__icontains=search_query)
        )
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        sermons = sermons.filter(series__category_id=category_id)
    
    # Pagination
    paginator = Paginator(sermons, 12)  # Show 12 sermons per page
    page = request.GET.get('page')
    sermons = paginator.get_page(page)
    
    # Get categories for filter dropdown
    categories = SermonCategory.objects.all()
    
    context = {
        'sermons': sermons,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_id
    }
    return render(request, 'services/sermons/home_sermons.html', context)

@login_required
def sermon_detail(request, sermon_slug):
    sermon = get_object_or_404(Sermon, slug=sermon_slug)
    
    # Get related sermons from same series or by same preacher
    related_sermons = Sermon.objects.filter(
        Q(series=sermon.series) | Q(preacher=sermon.preacher)
    ).exclude(id=sermon.id).order_by('-date_preached')[:3]
    
    context = {
        'sermon': sermon,
        'related_sermons': related_sermons,
        'user_has_liked': sermon.likes.filter(id=request.user.id).exists()
    }
    return render(request, 'services/sermons/sermon_detail.html', context)

@login_required
def like_sermon(request, sermon_slug):
    sermon = get_object_or_404(Sermon, slug=sermon_slug)
    if request.user in sermon.likes.all():
        sermon.likes.remove(request.user)
        liked = False
    else:
        sermon.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': sermon.likes.count()})

@login_required
def save_note(request, sermon_slug):
    if request.method == 'POST':
        sermon = get_object_or_404(Sermon, slug=sermon_slug)
        note = SermonNote.objects.create(
            sermon=sermon,
            user=request.user,
            content=request.POST.get('content')
        )
        messages.success(request, 'Note saved successfully!')
    return redirect('services:sermon_detail', sermon_slug=sermon_slug)

def sermon_categories(request):
    categories = SermonCategory.objects.all()
    return render(request, 'services/sermons/categories.html', {'categories': categories})

@login_required
def edit_sermon_category(request, category_slug):
    category = get_object_or_404(SermonCategory, slug=category_slug)
    if request.method == 'POST':
        form = SermonCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('services:categories')
    else:
        form = SermonCategoryForm(instance=category)
    return render(request, 'services/sermons/edit_category.html', {'form': form})

@login_required
def delete_sermon_category(request, category_slug):
    category = get_object_or_404(SermonCategory, slug=category_slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('services:categories')

@login_required
def bible_study_list(request):
    studies = BibleStudy.objects.all().order_by('-start_date')
    return render(request, 'services/bible_study_list.html', {'studies': studies})

@login_required
def bible_study_detail(request, pk):
    study = get_object_or_404(BibleStudy, pk=pk)
    return render(request, 'services/bible_study_detail.html', {'study': study})

@login_required
def create_bible_study(request):
    if request.method == 'POST':
        form = BibleStudyForm(request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.leader = request.user
            study.save()
            messages.success(request, 'Bible study created successfully!')
            return redirect('services:bible_study_list')
    else:
        form = BibleStudyForm()
    return render(request, 'services/create_bible_study.html', {'form': form})

@login_required
def worship_service_list(request):
    services_list = WorshipService.objects.all().order_by('-date')
    
    # Set up pagination

    context = {
        'services': services_list,
    }
    
    return render(request, 'services/worship/worship_services_list.html', context)



@login_required
def youth_ministry_list(request):
    events = YouthEvent.objects.all().order_by('-date')
    return render(request, 'services/youth/youth_events.html', {'events': events})

@login_required
def youth_event_detail(request, pk):
    event = get_object_or_404(YouthEvent, pk=pk)
    return render(request, 'services/youth/youth_event_detail.html', {'event': event})

@login_required
def create_youth_event(request):
    if request.method == 'POST':
        form = YouthEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Youth event created successfully!')
            return redirect('services:youth_ministry_list')
    else:
        form = YouthEventForm()
    return render(request, 'services/youth_programs/event_form.html', {'form': form})

@login_required
def children_ministry_list(request):
    programs = ChildrenProgram.objects.all().order_by('-date')
    return render(request, 'services/children/children_programs.html', {'programs': programs})

@login_required
def register_child(request):
    if request.method == 'POST':
        form = ChildRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.parent = request.user
            registration.save()
            messages.success(request, 'Child registered successfully!')
            return redirect('services:children_ministry_list')
    else:
        form = ChildRegistrationForm()
    return render(request, 'services/register_child.html', {'form': form})

@login_required
def create_children_program(request):
    if request.method == 'POST':
        form = ChildrenProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, 'Children\'s program created successfully!')
            return redirect('services:children_ministry_list')
    else:
        form = ChildrenProgramForm()
    return render(request, 'services/children/create_children_program.html', {'form': form})

class CouplesHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'services/couples/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = CoupleEvent.objects.filter(created_at__gte=timezone.now()).order_by('created_at')[:5]
        return context

class CoupleProfileView(LoginRequiredMixin, DetailView):
    model = CoupleProfile
    template_name = 'services/couples/profile.html'
    context_object_name = 'couple'

    def get_object(self):
        return get_object_or_404(CoupleProfile, partner_name=self.request.user)

class CoupleEventList(LoginRequiredMixin, ListView):
    model = CoupleEvent
    template_name = 'services/couples/event_list.html'
    context_object_name = 'events'

class CoupleEventDetail(LoginRequiredMixin, DetailView):
    model = CoupleEvent
    template_name = 'services/couples/event_detail.html'
    context_object_name = 'event'

@login_required
def event_registration(request, slug):
    event = get_object_or_404(CoupleEvent, slug=slug)
    couple = get_object_or_404(CoupleProfile, partner1=request.user)
    
    if request.method == 'POST':
        EventRegistration.objects.create(event=event, couple=couple)
        messages.success(request, 'Successfully registered for the event!')
        return redirect('services:event_detail', slug=slug)

class CounselingSessionList(LoginRequiredMixin, ListView):
    model = CounselingSession
    template_name = 'services/couples/counseling_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        couple = get_object_or_404(CoupleProfile, partner_name=self.request.user)
        return CounselingSession.objects.filter(couple=couple)

class CoupleResourceList(LoginRequiredMixin, ListView):
    model = CoupleResource
    template_name = 'services/couples/resource_list.html'
    context_object_name = 'resources'

@login_required
def add_journal_entry(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            couple = get_object_or_404(CoupleProfile, partner1=request.user)
            entry.couple = couple
            entry.save()
            messages.success(request, 'Journal entry added successfully!')
            return redirect('services:couple_journal')
    else:
        form = JournalEntryForm()
    return render(request, 'services/couples/add_journal_entry.html', {'form': form})

class PrayerRequestList(LoginRequiredMixin, ListView):
    model = CouplePrayerRequest
    template_name = 'services/couples/prayer_list.html'
    context_object_name = 'prayers'

    def get_queryset(self):
        couple = get_object_or_404(CoupleProfile, partner_name=self.request.user)
        return CouplePrayerRequest.objects.filter(couple=couple)

class DateNightIdeaList(LoginRequiredMixin, ListView):
    model = DateNightIdea
    template_name = 'services/couples/date_ideas.html'
    context_object_name = 'ideas'

@login_required
def events_view(request):
    upcoming_events = Event.objects.filter(
        start_date__gte=timezone.now()
    ).order_by('start_date')
    
    return render(request, 'events/event_list.html', {
        'upcoming_events': upcoming_events
    })

@login_required
def testimony_list(request):
    testimonies = Testimony.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'services/testimonies/testimony_list.html', {
        'testimonies': testimonies
    })

@login_required
def create_testimony(request):
    if request.method == 'POST':
        form = TestimonyForm(request.POST)
        if form.is_valid():
            testimony = form.save(commit=False)
            testimony.author = request.user
            testimony.save()
            messages.success(request, 'Your testimony has been submitted for review.')
            return redirect('services:testimony_list')
    else:
        form = TestimonyForm()
    
    return render(request, 'services/testimonies/create_testimony.html', {'form': form})

@login_required
def approve_testimony(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to approve testimonies.')
        return redirect('services:testimony_list')
        
    testimony = get_object_or_404(Testimony, pk=pk)
    testimony.is_approved = True
    testimony.save()
    messages.success(request, 'Testimony approved successfully!')
    return redirect('services:testimony_list')

@login_required
def add_testimony(request, pk):
    prayer_request = get_object_or_404(PrayerRequest, pk=pk)
    if request.method == 'POST':
        form = TestimonyForm(request.POST)
        if form.is_valid():
            testimony = form.save(commit=False)
            testimony.prayer_request = prayer_request
            testimony.author = request.user
            testimony.save()
            messages.success(request, 'Testimony added successfully!')
            return redirect('services:prayer_request_detail', pk=pk)
    else:
        form = TestimonyForm()
    return render(request, 'services/add_testimony.html', {'form': form, 'prayer_request': prayer_request})

@login_required
def prayer_requests_list(request):
    """List all prayer requests"""
    prayer_requests = PrayerRequest.objects.filter(
        Q(requester=request.user) | Q(is_private=False)
    ).order_by('-created_at')
    return render(request, 'services/prayer_requests/prayer_requests.html', {
        'prayer_requests': prayer_requests
    })

@login_required
def create_prayer_request(request):
    """Create a new prayer request"""
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            prayer_request = form.save(commit=False)
            prayer_request.author = request.user
            prayer_request.save()
            messages.success(request, 'Prayer request created successfully!')
            return redirect('services:prayer_requests')
    else:
        form = PrayerRequestForm()
    return render(request, 'services/prayer_requests/create_prayer_request.html', {'form': form})

@login_required
def prayer_request_detail(request, pk):
    """View a specific prayer request"""
    prayer_request = get_object_or_404(PrayerRequest, pk=pk)
    if prayer_request.is_private and prayer_request.author != request.user:
        messages.error(request, 'You do not have permission to view this prayer request.')
        return redirect('services:prayer_requests')
    
    updates = prayer_request.updates.all().order_by('-created_at')
    return render(request, 'services/prayer_requests/request_detail.html', {
        'prayer_request': prayer_request,
        'updates': updates
    })

@login_required
def add_prayer_update(request, pk):
    """Add an update to a prayer request"""
    prayer_request = get_object_or_404(PrayerRequest, pk=pk)
    if request.method == 'POST':
        form = PrayerUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.prayer_request = prayer_request
            update.author = request.user
            update.save()
            messages.success(request, 'Update added successfully!')
    return redirect('services:prayer_request_detail', pk=pk)

@login_required
def toggle_prayer_warrior(request, pk):
    """Toggle prayer warrior status for a prayer request"""
    prayer_request = get_object_or_404(PrayerRequest, pk=pk)
    if request.user in prayer_request.prayer_warriors.all():
        prayer_request.prayer_warriors.remove(request.user)
        messages.success(request, 'You are no longer praying for this request.')
    else:
        prayer_request.prayer_warriors.add(request.user)
        messages.success(request, 'You are now praying for this request.')
    return redirect('services:prayer_request_detail', pk=pk)

@login_required
def small_groups_list(request):
    """List all small groups"""
    groups = SmallGroup.objects.filter(is_accepting_members=True).order_by('name')
    return render(request, 'services/small_groups/small_groups.html', {'groups': groups})

@login_required
def create_small_group(request):
    """Create a new small group"""
    if request.method == 'POST':
        form = SmallGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.leader = request.user
            group.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Small group created successfully!')
            return redirect('services:small_groups')
    else:
        form = SmallGroupForm()
    return render(request, 'services/small_groups/create_small_groups.html', {'form': form})

@login_required
def small_group_detail(request, pk):
    """View details of a specific small group"""
    group = get_object_or_404(SmallGroup, pk=pk)
    is_member = request.user in group.members.all()
    is_leader = request.user == group.leaders
    return render(request, 'services/small_groups/details.html', {
        'group': group,
        'is_member': is_member,
        'is_leader': is_leader
    })

@login_required
def join_small_group(request, pk):
    """Join a small group"""
    group = get_object_or_404(SmallGroup, pk=pk)
    if request.user in group.members.all():
        messages.warning(request, 'You are already a member of this group.')
    else:
        group.members.add(request.user)
        messages.success(request, f'You have joined {group.name}!')
    return redirect('services:small_group_detail', pk=pk)

@login_required
def leave_small_group(request, pk):
    """Leave a small group"""
    group = get_object_or_404(SmallGroup, pk=pk)
    if request.user == group.leader:
        messages.error(request, 'Group leaders cannot leave their own group.')
    elif request.user in group.members.all():
        group.members.remove(request.user)
        messages.success(request, f'You have left {group.name}.')
    return redirect('services:small_groups')

@login_required
def add_sermon(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add sermons.')
        return redirect('services:sermon_list')
        
    if request.method == 'POST':
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            sermon = form.save(commit=False)
            sermon.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Sermon added successfully!')
            return redirect('services:sermon_detail', sermon_slug=sermon.slug)
    else:
        form = SermonForm()
    
    return render(request, 'services/sermons/add_sermon.html', {
        'form': form,
        'title': 'Add New Sermon'
    })

@login_required
def testimony_detail(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    
    # Only show approved testimonies or user's own testimonies
    if not testimony.is_approved and testimony.author != request.user and not request.user.is_staff:
        messages.error(request, "This testimony is not yet approved.")
        return redirect('services:testimony_list')
    
    context = {
        'testimony': testimony,
        'can_approve': request.user.is_staff and not testimony.is_approved,
    }
    return render(request, 'services/testimonies/testimony_detail.html', context)


@login_required
def create_reading_plan(request):
    if request.method == 'POST':
        form = BibleReadingPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.couple = request.user.couple_profile
            plan.save()
            messages.success(request, 'Reading plan created successfully!')
            return redirect('services:reading_plan_detail', pk=plan.pk)
    else:
        form = BibleReadingPlanForm()

    return render(request, 'services/couples/create_reading_plan.html', {
        'form': form,
        'profile': request.user.couple_profile,
    })


@login_required
def update_reading_progress(request, pk):
    plan = get_object_or_404(BibleReadingPlan, pk=pk, couple=request.user.couple_profile)

    if request.method == 'POST':
        chapters_read = int(request.POST.get('chapters_read', 0))
        if chapters_read > 0:
            plan.completed_chapters = min(plan.total_chapters, plan.completed_chapters + chapters_read)
            plan.save()

            # Update reading streak
            request.user.couple_profile.update_reading_streak()

            messages.success(request, f'Marked {chapters_read} chapters as read!')

    return redirect('services:reading_plan_detail', pk=pk)


@login_required
def reading_plan_detail(request, pk):
    profile = request.user.couple_profile
    plan = get_object_or_404(BibleReadingPlan, pk=pk, couple=profile)
    return render(request, 'services/couples/reading_plan_detail.html', {
        'plan': plan,
        'profile': profile,
    })


@login_required
def create_prayer_request(request):
    profile = request.user.couple_profile
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            prayer = form.save(commit=False)
            prayer.couple = profile
            prayer.save()
            messages.success(request, 'Prayer request created successfully!')
            return redirect('services:couple_prayers')
    else:
        form = PrayerRequestForm()

    return render(request, 'services/couples/prayer_request_form.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def prayer_request_detail(request, pk):
    profile = request.user.couple_profile
    prayer = get_object_or_404(PrayerRequest, pk=pk, couple=profile)
    return render(request, 'services/couples/prayer_request_detail.html', {
        'prayer': prayer,
        'profile': profile,
    })


@login_required
def update_prayer_request(request, pk):
    profile = request.user.couple_profile
    prayer = get_object_or_404(PrayerRequest, pk=pk, couple=profile)

    if request.method == 'POST':
        form = PrayerRequestForm(request.POST, instance=prayer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prayer request updated successfully!')
            return redirect('services:prayer_request_detail', pk=pk)
    else:
        form = PrayerRequestForm(instance=prayer)

    return render(request, 'services/couples/prayer_request_form.html', {
        'form': form,
        'prayer': prayer,
        'profile': profile,
    })


@login_required
def counseling_request(request):
    profile = request.user.couple_profile
    if request.method == 'POST':
        form = CounselingRequestForm(request.POST)
        if form.is_valid():
            counseling = form.save(commit=False)
            counseling.couple = profile
            counseling.save()
            messages.success(request, 'Counseling request submitted successfully!')
            return redirect('services:couple_profile')
    else:
        form = CounselingRequestForm()

    return render(request, 'services/couples/counseling_request.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def reading_plan_detail(request, pk):
    profile = request.user.couple_profile
    plan = get_object_or_404(BibleReadingPlan, pk=pk, couple=profile)
    return render(request, 'services/couples/reading_plan_detail.html', {
        'plan': plan,
        'profile': profile,
    })


@login_required
def create_prayer_request(request):
    profile = request.user.couple_profile
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            prayer = form.save(commit=False)
            prayer.couple = profile
            prayer.save()
            messages.success(request, 'Prayer request created successfully!')
            return redirect('services:couple_prayers')
    else:
        form = PrayerRequestForm()

    return render(request, 'services/couples/prayer_request_form.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def prayer_request_detail(request, pk):
    profile = request.user.couple_profile
    prayer = get_object_or_404(PrayerRequest, pk=pk, couple=profile)
    return render(request, 'services/couples/prayer_request_detail.html', {
        'prayer': prayer,
        'profile': profile,
    })


@login_required
def update_prayer_request(request, pk):
    profile = request.user.couple_profile
    prayer = get_object_or_404(PrayerRequest, pk=pk, couple=profile)

    if request.method == 'POST':
        form = PrayerRequestForm(request.POST, instance=prayer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prayer request updated successfully!')
            return redirect('services:prayer_request_detail', pk=pk)
    else:
        form = PrayerRequestForm(instance=prayer)

    return render(request, 'services/couples/prayer_request_form.html', {
        'form': form,
        'prayer': prayer,
        'profile': profile,
    })


@login_required
def couple_reading_plans(request):
    # Check if user has a profile
    if not hasattr(request.user, 'couple_profile'):
        messages.info(request, 'Please create your couple profile first to access reading plans.')
        return redirect('services:create_couple_profile')

    profile = request.user.couple_profile
    reading_plans = BibleReadingPlan.objects.filter(couples=profile).annotate(
        completion_percentage=models.F('completed_chapters') * 100.0 / models.F('total_chapters')
    ).order_by('-created_at')

    # Calculate statistics
    total_plans = reading_plans.count()
    completed_plans = reading_plans.filter(completed_chapters=models.F('total_chapters')).count()
    active_plans = reading_plans.filter(
        completed_chapters__lt=models.F('total_chapters'),
        end_date__gte=timezone.now().date()
    ).count()

    # Get plans by type
    daily_plans = reading_plans.filter(plan_type='DAILY').count()
    weekly_plans = reading_plans.filter(plan_type='WEEKLY').count()
    topical_plans = reading_plans.filter(plan_type='TOPICAL').count()

    context = {
        'profile': profile,
        'reading_plans': reading_plans,
        'statistics': {
            'total_plans': total_plans,
            'completed_plans': completed_plans,
            'active_plans': active_plans,
            'reading_streak': profile.reading_streak,
            'plan_types': {
                'daily': daily_plans,
                'weekly': weekly_plans,
                'topical': topical_plans,
            }
        },
        'current_date': timezone.now().date(),
    }

    return render(request, 'services/couples/reading_plan_form.html', context)


@login_required
def create_reading_plan(request):
    if not hasattr(request.user, 'couple_profile'):
        messages.warning(request, 'Please create your couple profile first to create reading plans.')
        return redirect('services:create_couple_profile')

    profile = request.user.couple_profile

    if request.method == 'POST':
        form = BibleReadingPlanForm(request.POST)
        if form.is_valid():
            try:
                plan = form.save(commit=False)

                # Set required fields
                plan.slug = slugify(plan.title)

                # Calculate duration in days
                if plan.end_date and plan.start_date:
                    duration = (plan.end_date - plan.start_date).days
                    plan.duration_days = max(duration, 1)  # Ensure minimum 1 day

                # Validate dates
                if plan.end_date and plan.end_date < plan.start_date:
                    messages.error(request, 'End date cannot be before start date.')
                    raise ValueError("Invalid date range")

                if plan.total_chapters <= 0:
                    messages.error(request, 'Total chapters must be greater than zero.')
                    raise ValueError("Invalid chapter count")

                plan.save()
                plan.couples.add(profile)

                # Update reading streak
                profile.update_reading_streak()

                messages.success(
                    request,
                    f'Reading plan "{plan.title}" created successfully! '
                    f'Your {plan.get_plan_type_display().lower()} plan starts on {plan.start_date.strftime("%B %d, %Y")}. '
                    f'You have {plan.total_chapters} chapters to complete.'
                )
                return redirect('services:couple_reading_plans')

            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            # Show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
    else:
        # Initialize form with default values
        form = BibleReadingPlanForm(initial={
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date() + timezone.timedelta(days=30),
            'plan_type': 'DAILY',
        })

    context = {
        'form': form,
        'profile': profile,
        'existing_plans': BibleReadingPlan.objects.filter(couples=profile).count(),
        'recent_plans': BibleReadingPlan.objects.filter(couples=profile).order_by('-created_at')[:3],
    }

    return render(request, 'services/couples/create_reading_plan.html', context)


class CoupleProfileDetailView(LoginRequiredMixin, DetailView):
    model = CoupleProfile
    template_name = 'services/couples/profile_detail.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()

            # Show appropriate messages based on profile status
            if self.object.status == 'pending':
                messages.info(request, 'Your profile is pending approval from the admin.')
            elif self.object.status == 'rejected':
                messages.warning(request, f'Your profile was rejected. Reason: {self.object.rejection_reason}')

            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        except CoupleProfile.DoesNotExist:
            messages.warning(request, 'Please create your couple profile first.')
            return redirect('services:create_couple_profile')

    def get_object(self):
        return get_object_or_404(CoupleProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        # Calculate marriage duration
        marriage_duration = timezone.now().date() - profile.anniversary
        years = marriage_duration.days // 365
        months = (marriage_duration.days % 365) // 30

        # Get activity statistics
        context.update({
            # Profile Status
            'profile_status': {
                'status': profile.get_status_display(),
                'is_approved': profile.is_approved,
                'approval_date': profile.approval_date,
                'approved_by': profile.approved_by,
                'rejection_reason': profile.rejection_reason if profile.status == 'rejected' else None,
            },

            # Marriage Info
            'marriage_info': {
                'duration_years': years,
                'duration_months': months,
                'stage': profile.get_marriage_stage_display(),
            },

            # Activity Summary
            'reading_plans': BibleReadingPlan.objects.filter(couples=profile).annotate(
                completion_percentage=models.F('completed_chapters') * 100.0 / models.F('total_chapters')
            )[:3],

            'upcoming_events': CoupleEvent.objects.filter(
                couples=profile,
                date__gte=timezone.now()
            ).order_by('date')[:3],

            'recent_prayers': PrayerRequest.objects.filter(
                couple=profile
            ).order_by('-created_at')[:3],

            # Statistics
            'statistics': {
                'total_events': CoupleEvent.objects.filter(couples=profile).count(),
                'reading_streak': profile.reading_streak,
                'prayer_requests': PrayerRequest.objects.filter(couple=profile).count(),
                'answered_prayers': PrayerRequest.objects.filter(
                    couple=profile,
                    status='answered'
                ).count(),
            },
        })
        return context

def youth_events_list(request):
    youth_events = YouthEvent.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'time')

    return render(request, 'services/youth/youth_events.html', {
        'youth_events': youth_events
    })


@login_required
def add_video_comment(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Sermon, id=video_id)  # Using Content instead of Video
        content = request.POST.get('content')
        if content:
            Comments.objects.create(  # Using Comments instead of VideoComment
                video=video,
                user=request.user,
                content=content
            )
            messages.success(request, 'Comment added successfully!')
        return redirect('services:sermon_details', video_id=video.id)
    return redirect('services:sermon_details', video_id=video_id)



@require_POST
def toggle_ministry_membership(request, ministry_id):
    ministry = get_object_or_404(WomensMinistry, id=ministry_id)
    if request.user in ministry.members.all():
        ministry.members.remove(request.user)
        status = 'removed'
    else:
        ministry.members.add(request.user)
        status = 'added'
    return JsonResponse({'status': status})

@require_POST
def toggle_event_attendance(request, event_id):
    event = get_object_or_404(MinistryEvent, id=event_id)
    if request.user in event.attendees.all():
        event.attendees.remove(request.user)
        status = 'removed'
    else:
        event.attendees.add(request.user)
        status = 'added'
    return JsonResponse({'status': status})


def mens_ministry_list(request):
    ministries = MensMinistry.objects.filter(is_active=True)
    context = {
        'ministries': ministries,
        'section': 'mens_ministry'
    }
    return render(request, 'services/mens_ministry/list.html', context)


def mens_ministry_detail(request, slug):
    ministry = get_object_or_404(MensMinistry, slug=slug)
    upcoming_events = ministry.events.filter(
        date__gte=timezone.now()
    ).order_by('date')
    past_events = ministry.events.filter(
        date__lt=timezone.now()
    ).order_by('-date')

    context = {
        'ministry': ministry,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'section': 'mens_ministry'
    }
    return render(request, 'services/mens_ministry/detail.html', context)


@login_required
def mens_ministry_create(request):
    if request.method == 'POST':
        form = MensMinistryForm(request.POST, request.FILES)
        if form.is_valid():
            ministry = form.save(commit=False)
            ministry.leader = request.user
            ministry.save()
            messages.success(request, "Men's ministry created successfully!")
            return redirect('services:mens_ministry_detail', slug=ministry.slug)
    else:
        form = MensMinistryForm()

    return render(request, 'services/mens_ministry/form.html', {
        'form': form,
        'action': 'Create',
        'section': 'mens_ministry'
    })


@login_required
def mens_event_create(request, ministry_slug):
    ministry = get_object_or_404(MensMinistry, slug=ministry_slug)

    if request.user != ministry.leader:
        messages.error(request, "You don't have permission to create events.")
        return redirect('services:mens_ministry_detail', slug=ministry_slug)

    if request.method == 'POST':
        form = MensEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.ministry = ministry
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('services:mens_ministry_detail', slug=ministry_slug)
    else:
        form = MensEventForm()

    return render(request, 'services/mens_ministry/event_form.html', {
        'form': form,
        'ministry': ministry,
        'action': 'Create',
        'section': 'mens_ministry'
    })


def youth_program_list(request):
    programs = YouthProgram.objects.filter(is_active=True)
    age_groups = dict(YouthProgram.AGE_GROUP_CHOICES)
    program_types = dict(YouthProgram.PROGRAM_TYPE_CHOICES)

    # Filter by age group and program type
    age_group = request.GET.get('age_group')
    program_type = request.GET.get('program_type')

    if age_group:
        programs = programs.filter(age_group=age_group)
    if program_type:
        programs = programs.filter(program_type=program_type)

    context = {
        'programs': programs,
        'age_groups': age_groups,
        'program_types': program_types,
        'selected_age_group': age_group,
        'selected_program_type': program_type,
    }
    return render(request, 'services/youth_programs/list.html', context)


def youth_program_detail(request, slug):
    program = get_object_or_404(YouthProgram, slug=slug)

    # Get upcoming and past events
    upcoming_events = program.events.filter(
        date__gte=timezone.now()
    ).order_by('date')

    past_events = program.events.filter(
        date__lt=timezone.now()
    ).order_by('-date')

    # Get member status for the current user
    is_member = request.user in program.members.all() if request.user.is_authenticated else False

    # Get event statuses for the current user
    if request.user.is_authenticated:
        event_statuses = {}
        for event in upcoming_events:
            try:
                attendee = YouthEventAttendee.objects.get(event=event, user=request.user)
                event_statuses[event.id] = {
                    'is_attending': True,
                    'permission_slip_submitted': attendee.permission_slip_submitted,
                    'payment_completed': attendee.payment_completed
                }
            except YouthEventAttendee.DoesNotExist:
                event_statuses[event.id] = {
                    'is_attending': False,
                    'permission_slip_submitted': False,
                    'payment_completed': False
                }
    else:
        event_statuses = {}

    context = {
        'program': program,
        'slug': slug,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'is_member': is_member,
        'event_statuses': event_statuses,
        'can_edit': request.user.is_authenticated and (
                request.user == program.leader or
                request.user.is_staff
        ),
        'member_count': program.members.count(),
        'has_space': program.has_space(),
    }

    return render(request, 'services/youth_programs/detail.html')


@login_required
def youth_program_create(request):
    if request.method == 'POST':
        form = YouthProgramForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            program.leader = request.user

            # Save first to generate slug
            program.save()

            # Now save many-to-many fields
            form.save_m2m()

            messages.success(request, 'Youth program created successfully!')
            return redirect(program.get_absolute_url())  # Use get_absolute_url instead
    else:
        form = YouthProgramForm()

    return render(request, 'services/youth/form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def youth_program_edit(request, slug):
    program = get_object_or_404(YouthProgram, slug=slug)

    if request.user != program.leader:
        messages.error(request, "You don't have permission to edit this program.")
        return redirect('services:youth_program_detail', slug=slug)

    if request.method == 'POST':
        form = YouthProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            program = form.save(commit=False)
            # Update slug if title changed
            new_slug = slugify(program.title)
            if new_slug != program.slug:
                base_slug = new_slug
                counter = 1
                while YouthProgram.objects.filter(slug=new_slug).exists():
                    new_slug = f"{base_slug}-{counter}"
                    counter += 1
                program.slug = new_slug
            program.save()
            messages.success(request, 'Youth program updated successfully!')
            return redirect('services:youth_program_detail', slug=program.slug)
    else:
        form = YouthProgramForm(instance=program)

    return render(request, 'services/youth_programs/form.html', {
        'form': form,
        'program': program,
        'action': 'Edit'
    })


# Rest of your views remain the same...


@login_required
def youth_program_create(request):
    if request.method == 'POST':
        form = YouthProgramForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            program.leader = request.user
            program.save()
            messages.success(request, 'Youth program created successfully!')
            return redirect('services:youth_program_detail', slug=program.slug)
    else:
        form = YouthProgramForm()

    return render(request, 'services/youth_programs/form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def youth_event_create(request, program_slug):
    program = get_object_or_404(YouthProgram, slug=program_slug)

    if request.user != program.leader:
        messages.error(request, "You don't have permission to create events.")
        return redirect('services:youth_program_detail', slug=program_slug)

    if request.method == 'POST':
        form = YouthEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.program = program
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('services:youth_program_detail', slug=program_slug)
    else:
        form = YouthEventForm()

    return render(request, 'services/youth_programs/event_form.html', {
        'form': form,
        'program': program,
        'action': 'Create'
    })


@login_required
@require_POST
def toggle_program_membership(request, program_id):
    program = get_object_or_404(YouthProgram, id=program_id)

    if request.user in program.members.all():
        program.members.remove(request.user)
        status = 'removed'
    else:
        if not program.has_space():
            return JsonResponse({
                'status': 'error',
                'message': 'This program has reached maximum capacity.'
            })
        program.members.add(request.user)
        status = 'added'

    return JsonResponse({'status': status})


@login_required
def process_payment(request, event_id):
    event = get_object_or_404(YouthEvent, id=event_id)
    attendee = get_object_or_404(YouthEventAttendee, event=event, user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.attendee = attendee
            payment.amount = event.cost

            # Integrate with payment gateway here
            try:
                # Process payment (example)
                payment_successful = process_payment_gateway(
                    amount=event.cost,
                    payment_method=form.cleaned_data['payment_method'],
                    user=request.user
                )

                if payment_successful:
                    payment.status = 'COMPLETED'
                    payment.save()
                    attendee.payment_completed = True
                    attendee.save()
                    messages.success(request, 'Payment processed successfully!')
                    return redirect('services:youth_event_detail', event_id=event.id)
            except PaymentError as e:
                messages.error(request, str(e))
    else:
        form = PaymentForm()

    return render(request, 'services/youth_programs/payment.html', {
        'form': form,
        'event': event,
        'attendee': attendee
    })


@login_required
def upload_permission_slip(request, event_id):
    event = get_object_or_404(YouthEvent, id=event_id)
    attendee = get_object_or_404(YouthEventAttendee, event=event, user=request.user)

    if request.method == 'POST':
        form = PermissionSlipForm(request.POST, request.FILES)
        if form.is_valid():
            permission_slip = form.save(commit=False)
            permission_slip.attendee = attendee
            permission_slip.save()

            attendee.permission_slip_submitted = True
            attendee.save()

            messages.success(request, 'Permission slip uploaded successfully!')
            return redirect('services:youth_event_detail', event_id=event.id)
    else:
        form = PermissionSlipForm()

    return render(request, 'services/youth_programs/permission_slip.html', {
        'form': form,
        'event': event
    })


@login_required
def record_attendance(request, event_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to record attendance.")
        return redirect('services:youth_event_detail', event_id=event_id)

    event = get_object_or_404(YouthEvent, id=event_id)

    if request.method == 'POST':
        attendee_id = request.POST.get('attendee_id')
        action = request.POST.get('action')

        attendee = get_object_or_404(YouthEventAttendee, id=attendee_id)
        attendance, created = AttendanceRecord.objects.get_or_create(
            event=event,
            attendee=attendee
        )

        if action == 'checkout':
            attendance.check_out_time = timezone.now()
            attendance.save()

        return JsonResponse({'status': 'success'})

    attendees = YouthEventAttendee.objects.filter(event=event)
    attendance_records = AttendanceRecord.objects.filter(event=event)

    return render(request, 'services/youth_programs/attendance.html', {
        'event': event,
        'attendees': attendees,
        'attendance_records': attendance_records
    })


@login_required
def attendance_report(request, event_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view attendance reports.")
        return redirect('services:youth_event_detail', event_id=event_id)

    event = get_object_or_404(YouthEvent, id=event_id)
    attendance_records = AttendanceRecord.objects.filter(event=event)

    # Generate Excel report
    if request.GET.get('format') == 'excel':
        workbook = generate_attendance_excel(event, attendance_records)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{event.title}_attendance.xlsx"'
        workbook.save(response)
        return response

    return render(request, 'services/youth_programs/attendance_report.html', {
        'event': event,
        'attendance_records': attendance_records
    })



@login_required
def seniors_events(request):
    upcoming_events = SeniorsEvent.objects.filter(date__gte=timezone.now()).order_by('date')
    past_events = SeniorsEvent.objects.filter(date__lt=timezone.now()).order_by('-date')

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'services/seniors_ministry/events.html', context)


@login_required
def seniors_event_create(request):
    if request.method == 'POST':
        form = SeniorsEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('services:seniors_event_detail', event_id=event.id)
    else:
        form = SeniorsEventForm()

    return render(request, 'services/seniors_ministry/form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def seniors_event_detail(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)
    context = {
        'event': event,
        'can_edit': request.user.is_staff,
        'is_registered': request.user in event.attendees.all(),
    }
    return render(request, 'services/seniors_ministry/detail.html', context)


@login_required
def seniors_event_register(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)

    if request.method == 'POST':
        if event.has_space() and event.is_registration_open():
            event.attendees.add(request.user)
            messages.success(request, 'Successfully registered for the event!')
        else:
            messages.error(request, 'Registration is not available.')

    return redirect('services:seniors_event_detail', event_id=event.id)


@login_required
def seniors_health(request):
    resources = HealthResource.objects.all().order_by('-created_at')
    return render(request, 'services/seniors_ministry/health.html', {
        'resources': resources
    })


@login_required
def health_resource_detail(request, resource_id):
    resource = get_object_or_404(HealthResource, id=resource_id)
    return render(request, 'services/seniors_ministry/health_resource_detail.html', {
        'resource': resource
    })


@login_required
def seniors_prayer(request):
    user_partnerships = PrayerPartner.objects.filter(user=request.user, active=True)
    available_partners = User.objects.exclude(
        id__in=user_partnerships.values_list('partner_id', flat=True)
    ).exclude(id=request.user.id)

    context = {
        'partnerships': user_partnerships,
        'available_partners': available_partners,
    }
    return render(request, 'services/seniors_ministry/prayer.html', context)


@login_required
def request_prayer_partner(request):
    if request.method == 'POST':
        partner_id = request.POST.get('partner_id')
        partner = get_object_or_404(User, id=partner_id)

        PrayerPartner.objects.create(
            user=request.user,
            partner=partner,
            active=True
        )

        messages.success(request, 'Prayer partnership request sent!')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def end_prayer_partnership(request):
    if request.method == 'POST':
        partnership_id = request.POST.get('partnership_id')
        partnership = get_object_or_404(PrayerPartner, id=partnership_id, user=request.user)

        partnership.active = False
        partnership.save()

        messages.success(request, 'Prayer partnership ended.')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def seniors_transportation(request):
    user_requests = TransportationRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'services/seniors_ministry/transportation.html', {
        'requests': user_requests
    })


@login_required
def transportation_request(request, activity_id):
    activity = get_object_or_404(SeniorsMinistry, id=activity_id)

    if request.method == 'POST':
        form = TransportationRequestForm(request.POST)
        if form.is_valid():
            transport = form.save(commit=False)
            transport.activity = activity
            transport.user = request.user
            transport.save()
            messages.success(request, 'Transportation request submitted successfully!')
            return redirect('services:seniors_ministry_detail', slug=activity.slug)
    else:
        form = TransportationRequestForm()

    return render(request, 'services/seniors_ministry/transportation_form.html', {
        'form': form,
        'activity': activity
    })


@login_required
def cancel_transportation(request, request_id):
    transport_request = get_object_or_404(TransportationRequest, id=request_id, user=request.user)
    transport_request.status = 'CANCELLED'
    transport_request.save()
    messages.success(request, 'Transportation request cancelled.')
    return redirect('services:seniors_transportation')


@login_required
def check_activity_space(request, activity_id):
    activity = get_object_or_404(SeniorsMinistry, id=activity_id)
    return JsonResponse({
        'has_space': activity.has_space(),
        'current_count': activity.members.count(),
        'max_participants': activity.max_participants
    })


@login_required
def get_event_attendees(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)
    attendees = list(event.attendees.values('id', 'first_name', 'last_name'))
    return JsonResponse({'attendees': attendees})


@login_required
def seniors_ministry_list(request):
    upcoming_events = SeniorsEvent.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')

    past_events = SeniorsEvent.objects.filter(
        date__lt=timezone.now()
    ).order_by('-date')

    # Check if there are any events
    if not upcoming_events.exists() and not past_events.exists():
        if request.user.is_staff:
            messages.info(request, 'No events found. Create your first event!')
            return redirect('services:seniors_event_create')
        else:
            messages.info(request, 'No events are currently scheduled. Please check back later.')
            return redirect('services:seniors_ministry_list')

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'services/seniors_ministry/list.html', context)


@login_required
def seniors_ministry_create(request):
    if request.method == 'POST':
        form = SeniorsMinistryForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.leader = request.user
            activity.save()
            messages.success(request, 'Senior\'s ministry activity created successfully!')
            return redirect('services:seniors_ministry_detail', slug=activity.slug)
    else:
        form = SeniorsMinistryForm()

    return render(request, 'services/seniors_ministry/form.html', {
        'form': form,
        'action': 'Create'
    })


def seniors_ministry_detail(request, slug):
    activity = get_object_or_404(SeniorsMinistry, slug=slug)
    context = {
        'activity': activity,
        'can_edit': request.user.is_authenticated and (
                request.user == activity.leader or request.user.is_staff
        ),
    }
    return render(request, 'services/seniors_ministry/detail.html', context)


@login_required
def seniors_ministry_edit(request, slug):
    activity = get_object_or_404(SeniorsMinistry, slug=slug)

    if request.user != activity.leader and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this activity.")
        return redirect('services:seniors_ministry_detail', slug=slug)

    if request.method == 'POST':
        form = SeniorsMinistryForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('services:seniors_ministry_detail', slug=activity.slug)
    else:
        form = SeniorsMinistryForm(instance=activity)

    return render(request, 'services/seniors_ministry/form.html', {
        'form': form,
        'activity': activity,
        'action': 'Edit'
    })


@login_required
def seniors_event_detail(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)
    context = {
        'event': event,
        'can_edit': request.user.is_staff,
        'is_registered': request.user in event.attendees.all(),
    }
    return render(request, 'services/seniors_ministry/detail.html', context)


@login_required
def seniors_event_register(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)

    if request.method == 'POST':
        if event.has_space() and event.is_registration_open():
            if request.user in event.attendees.all():
                event.attendees.remove(request.user)
                messages.success(request, 'Successfully unregistered from the event.')
            else:
                event.attendees.add(request.user)
                messages.success(request, 'Successfully registered for the event!')
        else:
            messages.error(request, 'Registration is not available.')

    return redirect('services:seniors_event_detail', event_id=event.id)


@login_required
def seniors_event_delete(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('services:seniors_event_detail', event_id=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('services:seniors_events')

    return render(request, 'services/seniors_ministry/event_confirm_delete.html', {
        'event': event
    })


@login_required
def get_event_attendees(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    attendees = list(event.attendees.values('id', 'first_name', 'last_name'))
    return JsonResponse({'attendees': attendees})


@login_required
def seniors_event_edit(request, event_id):
    event = get_object_or_404(SeniorsEvent, id=event_id)

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('services:seniors_event_detail', event_id=event_id)

    if request.method == 'POST':
        form = SeniorsEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('services:seniors_event_detail', event_id=event.id)
    else:
        form = SeniorsEventForm(instance=event)

    return render(request, 'services/seniors_ministry/event_form.html', {
        'form': form,
        'event': event,
        'action': 'Edit'
    })


# Add these prayer partnership views to your existing views

@login_required
def seniors_prayer(request):
    user_partnerships = PrayerPartner.objects.filter(
        models.Q(user=request.user) | models.Q(partner=request.user),
        active=True
    )
    available_partners = User.objects.exclude(
        id__in=user_partnerships.values_list('partner_id', flat=True)
    ).exclude(id=request.user.id)

    pending_requests = PrayerPartner.objects.filter(
        partner=request.user,
        active=True,
        accepted=False
    )

    context = {
        'partnerships': user_partnerships,
        'available_partners': available_partners,
        'pending_requests': pending_requests,
    }
    return render(request, 'services/seniors_ministry/prayer.html', context)


@login_required
def request_prayer_partner(request):
    if request.method == 'POST':
        partner_id = request.POST.get('partner_id')
        partner = get_object_or_404(User, id=partner_id)

        # Check if partnership already exists
        existing = PrayerPartner.objects.filter(
            models.Q(user=request.user, partner=partner) |
            models.Q(user=partner, partner=request.user),
            active=True
        ).exists()

        if existing:
            return JsonResponse({
                'status': 'error',
                'message': 'Partnership already exists'
            })

        PrayerPartner.objects.create(
            user=request.user,
            partner=partner,
            active=True,
            accepted=False
        )

        messages.success(request, 'Prayer partnership request sent!')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def accept_prayer_partnership(request, partnership_id):
    partnership = get_object_or_404(
        PrayerPartner,
        id=partnership_id,
        partner=request.user,
        active=True,
        accepted=False
    )

    if request.method == 'POST':
        partnership.accepted = True
        partnership.save()
        messages.success(request, 'Prayer partnership accepted!')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def decline_prayer_partnership(request, partnership_id):
    partnership = get_object_or_404(
        PrayerPartner,
        id=partnership_id,
        partner=request.user,
        active=True,
        accepted=False
    )

    if request.method == 'POST':
        partnership.active = False
        partnership.save()
        messages.success(request, 'Prayer partnership request declined.')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def end_prayer_partnership(request):
    if request.method == 'POST':
        partnership_id = request.POST.get('partnership_id')
        user_filter = models.Q(user=request.user) | models.Q(partner=request.user)
        partnership = get_object_or_404(
            PrayerPartner,
            user_filter,
            id=partnership_id,
            active=True
        )
        partnership.active = False
        partnership.save()

        messages.success(request, 'Prayer partnership ended.')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})



@login_required
def download_health_resource(request, resource_id):
    resource = get_object_or_404(HealthResource, id=resource_id)
    if resource.document:
        response = FileResponse(resource.document.open(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{resource.document.name}"'
        return response
    else:
        messages.error(request, 'No document available for download.')
        return redirect('services:seniors_health')


@login_required
def toggle_activity_membership(request, activity_id):
    activity = get_object_or_404(SeniorsMinistry, id=activity_id)

    if request.method == 'POST':
        if request.user in activity.members.all():
            activity.members.remove(request.user)
            status = 'removed'
            message = 'You have been removed from this activity.'
        else:
            if not activity.has_space():
                return JsonResponse({
                    'status': 'error',
                    'message': 'This activity has reached maximum capacity.'
                })
            activity.members.add(request.user)
            status = 'added'
            message = 'You have been added to this activity.'

        messages.success(request, message)
        return JsonResponse({
            'status': status,
            'current_count': activity.members.count(),
            'max_participants': activity.max_participants
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
def activity_members(request, activity_id):
    activity = get_object_or_404(SeniorsMinistry, id=activity_id)

    if not request.user.is_staff and request.user != activity.leader:
        messages.error(request, "You don't have permission to view member details.")
        return redirect('services:seniors_ministry_detail', slug=activity.slug)

    context = {
        'activity': activity,
        'members': activity.members.all().order_by('first_name', 'last_name')
    }
    return render(request, 'services/seniors_ministry/activity_members.html', context)


@login_required
def check_activity_space(request, activity_id):
    activity = get_object_or_404(SeniorsMinistry, id=activity_id)
    return JsonResponse({
        'has_space': activity.has_space(),
        'current_count': activity.members.count(),
        'max_participants': activity.max_participants
    })


def singles_ministry_list(request):
    activities = SinglesMinistry.objects.filter(is_active=True)

    # Filter by activity type, age group, and relationship status
    activity_type = request.GET.get('activity_type')
    age_group = request.GET.get('age_group')
    relationship_status = request.GET.get('relationship_status')

    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    if age_group:
        activities = activities.filter(age_group=age_group)
    if relationship_status:
        activities = activities.filter(relationship_status=relationship_status)

    context = {
        'activities': activities,
        'activity_types': dict(SinglesMinistry.ACTIVITY_CHOICES),
        'age_groups': dict(SinglesMinistry.AGE_GROUP_CHOICES),
        'relationship_statuses': dict(SinglesMinistry.RELATIONSHIP_STATUS_CHOICES),
        'selected_type': activity_type,
        'selected_age': age_group,
        'selected_status': relationship_status,
    }
    return render(request, 'services/singles_ministry/list.html', context)


@login_required
def singles_ministry_create(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create activities.")
        return redirect('services:singles_ministry_list')

    if request.method == 'POST':
        form = SinglesMinistryForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.leader = request.user
            activity.save()
            messages.success(request, 'Singles ministry activity created successfully!')
            return redirect('services:singles_ministry_detail', slug=activity.slug)
    else:
        form = SinglesMinistryForm()

    return render(request, 'services/singles_ministry/form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def singles_ministry_edit(request, slug):
    activity = get_object_or_404(SinglesMinistry, slug=slug)

    if request.user != activity.leader and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this activity.")
        return redirect('services:singles_ministry_detail', slug=slug)

    if request.method == 'POST':
        form = SinglesMinistryForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('services:singles_ministry_detail', slug=activity.slug)
    else:
        form = SinglesMinistryForm(instance=activity)

    return render(request, 'services/singles_ministry/form.html', {
        'form': form,
        'activity': activity,
        'action': 'Edit'
    })


def singles_ministry_detail(request, slug):
    activity = get_object_or_404(SinglesMinistry, slug=slug)
    upcoming_events = activity.events.filter(date__gte=timezone.now()).order_by('date')

    context = {
        'activity': activity,
        'upcoming_events': upcoming_events,
        'is_member': request.user in activity.members.all() if request.user.is_authenticated else False,
        'can_edit': request.user.is_authenticated and (
                request.user == activity.leader or request.user.is_staff
        ),
    }
    return render(request, 'services/singles_ministry/detail.html', context)


@login_required
def singles_events(request):
    upcoming_events = SinglesEvent.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')

    past_events = SinglesEvent.objects.filter(
        date__lt=timezone.now()
    ).order_by('-date')

    # Check if there are any events
    if not upcoming_events.exists() and not past_events.exists():
        if request.user.is_staff:
            messages.info(request, 'No events found. Create your first event!')
            return redirect('services:singles_event_create')
        else:
            messages.info(request, 'No events are currently scheduled. Please check back later.')
            return redirect('services:singles_ministry_list')

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'services/singles_ministry/events.html', context)


@login_required
def singles_event_create(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create events.")
        return redirect('services:singles_events')

    if request.method == 'POST':
        form = SinglesEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('services:singles_event_detail', event_id=event.id)
    else:
        form = SinglesEventForm()

    return render(request, 'services/singles_ministry/event_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def singles_event_detail(request, event_id):
    event = get_object_or_404(SinglesEvent, id=event_id)
    registration_form = SinglesEventRegistrationForm() if event.is_registration_open() else None

    context = {
        'event': event,
        'registration_form': registration_form,
        'is_registered': request.user in event.attendees.all(),
        'can_edit': request.user.is_staff,
        'now': timezone.now(),
    }
    return render(request, 'services/singles_ministry/event_detail.html', context)


@login_required
def singles_event_register(request, event_id):
    event = get_object_or_404(SinglesEvent, id=event_id)

    if request.method == 'POST':
        form = SinglesEventRegistrationForm(request.POST)
        if form.is_valid():
            if event.has_space() and event.is_registration_open():
                if request.user in event.attendees.all():
                    event.attendees.remove(request.user)
                    messages.success(request, 'Successfully unregistered from the event.')
                else:
                    event.attendees.add(request.user)
                    messages.success(request, 'Successfully registered for the event!')
            else:
                messages.error(request, 'Registration is not available.')

    return redirect('services:singles_event_detail', event_id=event.id)


@login_required
def mentorship_request(request):
    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            mentorship = form.save(commit=False)
            mentorship.mentee = request.user
            mentorship.save()
            messages.success(request, 'Mentorship request submitted successfully!')
            return redirect('services:singles_ministry_list')
    else:
        form = MentorshipRequestForm()

    return render(request, 'services/singles_ministry/mentorship_form.html', {
        'form': form
    })


@login_required
def mentorship_list(request):
    if request.user.is_staff:
        pending_requests = MentorshipRequest.objects.filter(status='PENDING')
        active_matches = MentorshipRequest.objects.filter(status='MATCHED')
    else:
        pending_requests = MentorshipRequest.objects.filter(
            Q(mentee=request.user) | Q(mentor=request.user)
        ).filter(status='PENDING')
        active_matches = MentorshipRequest.objects.filter(
            Q(mentee=request.user) | Q(mentor=request.user)
        ).filter(status='MATCHED')

    context = {
        'pending_requests': pending_requests,
        'active_matches': active_matches,
    }
    return render(request, 'services/singles_ministry/mentorship_list.html', context)


@login_required
def singles_resources(request):
    resources = SinglesResource.objects.all().order_by('-created_at')
    featured_resources = resources.filter(is_featured=True)

    # Filter by category
    category = request.GET.get('category')
    if category:
        resources = resources.filter(category=category)

    context = {
        'resources': resources,
        'featured_resources': featured_resources,
        'categories': dict(SinglesResource.CATEGORY_CHOICES),
        'selected_category': category,
    }
    return render(request, 'services/singles_ministry/resources.html', context)


@login_required
def toggle_activity_membership(request, activity_id):
    activity = get_object_or_404(SinglesMinistry, id=activity_id)

    if request.method == 'POST':
        if request.user in activity.members.all():
            activity.members.remove(request.user)
            status = 'removed'
            message = 'You have been removed from this activity.'
        else:
            if not activity.has_space():
                return JsonResponse({
                    'status': 'error',
                    'message': 'This activity has reached maximum capacity.'
                })
            activity.members.add(request.user)
            status = 'added'
            message = 'You have been added to this activity.'

        messages.success(request, message)
        return JsonResponse({
            'status': status,
            'current_count': activity.members.count(),
            'max_participants': activity.max_participants
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
def accept_mentorship(request, request_id):
    mentorship = get_object_or_404(
        MentorshipRequest,
        id=request_id,
        status='PENDING'
    )

    if request.method == 'POST':
        if request.user.is_staff:
            form = MentorshipMatchForm(request.POST, potential_mentors=User.objects.filter(is_staff=True))
            if form.is_valid():
                mentorship.mentor = form.cleaned_data['mentor']
                mentorship.status = 'MATCHED'
                mentorship.notes = form.cleaned_data['notes']
                mentorship.save()

                messages.success(
                    request,
                    f'Mentorship match created between {mentorship.mentee.get_full_name()} and {mentorship.mentor.get_full_name()}'
                )
                return redirect('services:singles_mentorship_list')
        else:
            messages.error(request, "You don't have permission to make mentorship matches.")

    return redirect('services:singles_mentorship_list')


@login_required
def decline_mentorship(request, request_id):
    mentorship = get_object_or_404(
        MentorshipRequest,
        id=request_id,
        status='PENDING'
    )

    if request.method == 'POST':
        if request.user.is_staff or request.user == mentorship.mentor:
            mentorship.status = 'CANCELLED'
            mentorship.save()
            messages.success(request, 'Mentorship request declined.')
        else:
            messages.error(request, "You don't have permission to decline this request.")

    return redirect('services:singles_mentorship_list')


@login_required
def complete_mentorship(request, request_id):
    mentorship = get_object_or_404(
        MentorshipRequest,
        id=request_id,
        status='MATCHED'
    )

    if request.method == 'POST':
        if request.user == mentorship.mentor or request.user == mentorship.mentee:
            mentorship.status = 'COMPLETED'
            mentorship.save()

            # Optional: Add completion notes
            completion_notes = request.POST.get('completion_notes')
            if completion_notes:
                mentorship.notes += f"\n\nCompletion Notes ({timezone.now()}):\n{completion_notes}"
                mentorship.save()

            messages.success(request, 'Mentorship marked as completed.')
        else:
            messages.error(request, "You don't have permission to complete this mentorship.")

    return redirect('services:singles_mentorship_list')


@login_required
def resource_detail(request, resource_id):
    resource = get_object_or_404(SinglesResource, id=resource_id)

    # Track resource views (optional)
    if not request.session.get(f'viewed_resource_{resource_id}'):
        request.session[f'viewed_resource_{resource_id}'] = True
        # You could add a views counter to your model if desired

    context = {
        'resource': resource,
        'related_resources': SinglesResource.objects.filter(
            category=resource.category
        ).exclude(id=resource.id)[:3],
        'can_edit': request.user.is_staff
    }
    return render(request, 'services/singles_ministry/resource_detail.html', context)


@login_required
def download_resource(request, resource_id):
    resource = get_object_or_404(SinglesResource, id=resource_id)

    if not resource.document:
        messages.error(request, 'No document available for download.')
        return redirect('services:singles_resource_detail', resource_id=resource_id)

    try:
        response = FileResponse(
            resource.document.open(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{resource.document.name}"'

        # Track downloads (optional)
        if not request.session.get(f'downloaded_resource_{resource_id}'):
            request.session[f'downloaded_resource_{resource_id}'] = True
            # You could add a downloads counter to your model if desired

        return response
    except Exception as e:
        messages.error(request, 'Error downloading the resource. Please try again.')
        return redirect('services:singles_resource_detail', resource_id=resource_id)