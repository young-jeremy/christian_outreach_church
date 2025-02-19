from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import *


def dashboard_view(request):
    categories = Category.objects.all()
    for category in categories:
        page_number = request.GET.get('page', 1)
        category_id = request.GET.get('category')
        contents = category.contents.all()
        paginator = Paginator(contents, 6)
        if category_id and int(category_id) == category.id:
            category.contents = paginator.get_page(page_number)
        else:
            category.contents = paginator.get_page(1)
    return render(request, 'dashboard/index.html', {'categories': categories})


@login_required
def sermons_view(request):
    sermons = Sermon.objects.all().order_by('-date')
    paginator = Paginator(sermons, 9)
    page = request.GET.get('page')
    sermons = paginator.get_page(page)
    return render(request, 'ministry/sermons.html', {'sermons': sermons})


@login_required
def bible_studies_view(request):
    studies = BibleStudy.objects.all().order_by('-video__created_at')
    paginator = Paginator(studies, 9)
    page = request.GET.get('page')
    studies = paginator.get_page(page)
    return render(request, 'ministry/bible_studies.html', {'studies': studies})


@login_required
def prayer_requests_view(request):
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            prayer_request = form.save(commit=False)
            prayer_request.requester = request.user
            prayer_request.save()
            return redirect('prayer_requests')
    else:
        form = PrayerRequestForm()

    prayer_requests = PrayerRequest.objects.filter(is_anonymous=False).order_by('-created_at')
    return render(request, 'community/prayer_requests.html', {
        'form': form,
        'prayer_requests': prayer_requests
    })


@login_required
def small_groups_view(request):
    groups = SmallGroup.objects.all()
    if request.method == 'POST':
        form = SmallGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.leader = request.user
            group.save()
            return redirect('small_groups')
    else:
        form = SmallGroupForm()
    return render(request, 'community/small_groups.html', {
        'groups': groups,
        'form': form
    })


@login_required
def events_view(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'community/events.html', {
        'events': events,
        'form': form
    })


@login_required
def devotionals_view(request):
    devotionals = Devotional.objects.all().order_by('-date')
    paginator = Paginator(devotionals, 7)
    page = request.GET.get('page')
    devotionals = paginator.get_page(page)
    return render(request, 'resources/devotionals.html', {'devotionals': devotionals})


@login_required
def missions_view(request):
    active_missions = Mission.objects.filter(end_date__gte=timezone.now()).order_by('start_date')
    past_missions = Mission.objects.filter(end_date__lt=timezone.now()).order_by('-end_date')
    return render(request, 'outreach/missions.html', {
        'active_missions': active_missions,
        'past_missions': past_missions
    })
