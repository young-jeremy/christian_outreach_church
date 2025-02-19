from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from services.forms import EventForm
from django.shortcuts import get_object_or_404
import time
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Event
from datetime import datetime, date


@login_required
def events_list(request):
    events = Event.objects.filter(is_published=True)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by type
    event_type = request.GET.get('type', '')
    if event_type:
        events = events.filter(event_type=event_type)

    # Filter by date
    filter_date = request.GET.get('date', 'upcoming')
    if filter_date == 'upcoming':
        events = events.filter(start_date__gte=timezone.now().date())
    elif filter_date == 'past':
        events = events.filter(start_date__lt=timezone.now().date())

    # Pagination
    paginator = Paginator(events, 9)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'events': events,
        'search_query': search_query,
        'current_type': event_type,
        'event_types': Event.EVENT_TYPES,
        'current_filter': filter_date,
    }
    return render(request, 'events/events_list.html', context)


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            
            # Convert dates to datetime for comparison
            start_datetime = timezone.make_aware(
                datetime.combine(event.start_date, event.start_time)
            )
            end_datetime = timezone.make_aware(
                datetime.combine(event.end_date, event.end_time)
            )
            
            # Compare datetime objects
            if end_datetime < start_datetime:
                messages.error(request, 'End date/time must be after start date/time')
                return render(request, 'events/create_event.html', {'form': form})
            
            event.creator = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {
        'form': form,
        'title': 'Create Event'
    })


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = request.user in event.participants.all()
    can_register = event.can_register(request.user)

    if request.method == 'POST' and can_register:
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            event.participants.add(request.user)
            messages.success(request, f'You have registered for {event.title}!')
            return redirect('events:event_detail', pk=pk)
    else:
        form = EventRegistrationForm()

    context = {
        'event': event,
        'is_registered': is_registered,
        'can_register': can_register,
        'form': form,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def cancel_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user not in event.participants.all():
        messages.error(request, 'You are not registered for this event.')
        return redirect('events:event_detail', pk=pk)

    if request.method == 'POST':
        event.participants.remove(request.user)
        messages.success(request, f'Your registration for {event.title} has been cancelled.')

    return redirect('events:event_detail', pk=pk)


@login_required
def downloaded_videos(request):
    videos = DownloadedVideo.objects.filter(user=request.user).order_by('-download_date')
    return render(request, 'videos/downloaded_videos.html', {'videos': videos})


@login_required
def live_streams_view(request):
    # Get current live streams
    live_streams = LiveStream.objects.filter(
        is_live=True
    ).order_by('-actual_start_time')

    # Get upcoming streams
    upcoming_streams = LiveStream.objects.filter(
        is_live=False,
        scheduled_time__gte=timezone.now()
    ).order_by('scheduled_time')

    # Get past streams
    past_streams = LiveStream.objects.filter(
        is_live=False,
        scheduled_time__lt=timezone.now()
    ).order_by('-scheduled_time')[:10]  # Show only last 10 past streams

    if request.method == 'POST':
        form = LiveStreamForm(request.POST, request.FILES)
        if form.is_valid():
            stream = form.save(commit=False)
            stream.streamer = request.user
            stream.stream_key = f"stream_{request.user.id}_{int(time.time())}"  # Generate unique stream key
            stream.save()
            messages.success(request, 'Stream scheduled successfully!')
            return redirect('events:live_stream_view')
    else:
        form = LiveStreamForm()

    context = {
        'live_streams': live_streams,
        'upcoming_streams': upcoming_streams,
        'past_streams': past_streams,
        'form': form
    }
    return render(request, 'events/index.html', context)


@login_required
def stream_detail_view(request, stream_id):
    stream = get_object_or_404(LiveStream, id=stream_id)
    return render(request, 'live_streams/stream.html', {'stream': stream})


@login_required
def start_stream(request, stream_id):
    stream = get_object_or_404(LiveStream, id=stream_id, streamer=request.user)
    if request.method == 'POST':
        stream.is_live = True
        stream.actual_start_time = timezone.now()
        stream.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def end_stream(request, stream_id):
    stream = get_object_or_404(LiveStream, id=stream_id, streamer=request.user)
    if request.method == 'POST':
        stream.is_live = False
        stream.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def missions_view(request):
    active_missions = Mission.objects.filter(end_date__gte=timezone.now()).order_by('start_date')
    past_missions = Mission.objects.filter(end_date__lt=timezone.now()).order_by('-end_date')
    return render(request, 'outreach/missions.html', {
        'active_missions': active_missions,
        'past_missions': past_missions
    })
