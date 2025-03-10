from outreach.models import Mission
from .forms import *
from services.forms import EventForm, EventRegistrationForm
import time
from datetime import datetime
from services.models import Event
from .models import LiveStream
from .forms import LiveStreamForm, StreamChatForm
import uuid
from django.conf import settings
from django.db.models import Q
from .models import ArchivedVideo, VideoCategory
from .forms import VideoUploadForm
from django.http import JsonResponse
from .models import PhotoAlbum, Photo
from .forms import PhotoAlbumForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import (
    AudioMessage, NewsArticle, Newsletter,
    Announcement, TestimonialVideo
)
from .forms import (
    AudioMessageForm, NewsArticleForm, NewsletterForm,
    AnnouncementForm, TestimonialVideoForm
)
import time
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone


from services.forms import EventForm
from .forms import *
from .forms import (
    AudioMessageForm, NewsArticleForm, NewsletterForm,
    AnnouncementForm, TestimonialVideoForm
)
from .forms import LiveStreamForm, StreamChatForm
from .forms import PhotoAlbumForm
from .forms import VideoUploadForm
from .models import ArchivedVideo, VideoCategory
from .models import (
    AudioMessage, NewsArticle, Newsletter,
    Announcement, TestimonialVideo
)
from .models import Event
from .models import LiveStream
from .models import PhotoAlbum, Photo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm


@login_required
def announcement_list(request):
    priority = request.GET.get('priority')
    announcements = Announcement.objects.select_related('created_by').order_by('-priority', '-start_date')

    if priority:
        announcements = announcements.filter(priority=priority)

    priorities = Announcement.PRIORITY_CHOICES

    context = {
        'announcements': announcements,
        'priorities': priorities,
    }
    return render(request, 'events/announcement/list.html', context)


@login_required
@permission_required('coc.add_announcement', raise_exception=True)
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully.')
            return redirect('events:announcement_list')
    else:
        form = AnnouncementForm()

    return render(request, 'events/announcement/create.html', {'form': form})


@login_required
@permission_required('coc.change_announcement', raise_exception=True)
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    # Check if user is the creator or has sufficient permissions
    if not (request.user == announcement.created_by or request.user.is_superuser):
        messages.error(request, 'You do not have permission to edit this announcement.')
        return redirect('events:announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated successfully.')
            return redirect('events:announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'events/announcement/create.html', {
        'form': form,
        'announcement': announcement
    })


@login_required
@permission_required('education.delete_announcement', raise_exception=True)
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    # Check if user is the creator or has sufficient permissions
    if not (request.user == announcement.created_by or request.user.is_superuser):
        messages.error(request, 'You do not have permission to delete this announcement.')
        return redirect('events:announcement_list')

    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully.')
        return redirect('events:announcement_list')

    return redirect('events:announcement_list')


@login_required
@permission_required('education.change_testimonialvideo', raise_exception=True)
def testimonial_edit(request, slug):
    testimonial = get_object_or_404(TestimonialVideo, slug=slug)

    # Check if user is the uploader or has sufficient permissions
    if not (request.user == testimonial.uploaded_by or request.user.is_superuser):
        messages.error(request, 'You do not have permission to edit this testimony.')
        return redirect('education:testimonial_detail', slug=slug)

    if request.method == 'POST':
        form = TestimonialVideoForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimony updated successfully.')
            return redirect('events:testimonial_detail', slug=testimonial.slug)
    else:
        form = TestimonialVideoForm(instance=testimonial)

    return render(request, 'events/testimonial/create.html', {
        'form': form,
        'testimonial': testimonial
    })


@login_required
@permission_required('coc.delete_testimonialvideo', raise_exception=True)
def testimonial_delete(request, slug):
    testimonial = get_object_or_404(TestimonialVideo, slug=slug)

    # Check if user is the uploader or has sufficient permissions
    if not (request.user == testimonial.uploaded_by or request.user.is_superuser):
        messages.error(request, 'You do not have permission to delete this testimony.')
        return redirect('events:testimonial_detail', slug=slug)

    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimony deleted successfully.')
        return redirect('events:testimonial_list')

    return render(request, 'events/testimonial/delete.html', {'testimonial': testimonial})


@login_required
@permission_required('coc.delete_audiomessage', raise_exception=True)
def audio_message_delete(request, slug):
    message = get_object_or_404(AudioMessage, slug=slug)

    # Check if user is the speaker or has sufficient permissions
    if not (request.user == message.speaker or request.user.is_superuser):
        messages.error(request, 'You do not have permission to delete this message.')
        return redirect('events:audio_message_detail', slug=slug)

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Audio message deleted successfully.')
        return redirect('events:audio_message_list')

    return render(request, 'events/audio_messages/delete.html', {'message': message})


@login_required
@permission_required('coc.change_audiomessage', raise_exception=True)
def audio_message_edit(request, slug):
    message = get_object_or_404(AudioMessage, slug=slug)

    # Check if user is the speaker or has sufficient permissions
    if not (request.user == message.speaker or request.user.is_superuser):
        messages.error(request, 'You do not have permission to edit this message.')
        return redirect('events:audio_message_detail', slug=slug)

    if request.method == 'POST':
        form = AudioMessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Audio message updated successfully.')
            return redirect('events:audio_message_detail', slug=message.slug)
    else:
        form = AudioMessageForm(instance=message)

    return render(request, 'events/audio_messages/create.html', {'form': form})


# Audio Message Views
@login_required
def audio_message_list(request):
    messages = AudioMessage.objects.all()
    paginator = Paginator(messages, 12)
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    return render(request, 'events/audio_messages/list.html', {'messages': messages})


@login_required
def audio_message_detail(request, slug):
    message = get_object_or_404(AudioMessage, slug=slug)
    message.view_count += 1
    message.save()
    return render(request, 'events/audio_messages/detail.html', {'message': message})


@permission_required('events.add_audiomessage')
def audio_message_create(request):
    if request.method == 'POST':
        form = AudioMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save()
            messages.success(request, 'Audio message uploaded successfully!')
            return redirect('events:audio_message_detail', slug=message.slug)
    else:
        form = AudioMessageForm()
    return render(request, 'events/audio_messages/create.html', {'form': form})


# News Article Views
@login_required
def news_list(request):
    articles = NewsArticle.objects.filter(is_published=True)
    featured = articles.filter(featured=True)[:5]
    recent = articles.filter(featured=False)[:10]
    return render(request, 'events/news/list.html', {
        'featured_articles': featured,
        'recent_articles': recent
    })


@login_required
def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    return render(request, 'events/news/detail.html', {'article': article})


@permission_required('coc.add_newsarticle')
def news_create(request):
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'News article created successfully!')
            return redirect('events:news_detail', slug=article.slug)
    else:
        form = NewsArticleForm()
    return render(request, 'events/news/create.html', {'form': form})


# Newsletter Views
@login_required
def newsletter_list(request):
    newsletters = Newsletter.objects.filter(is_published=True)
    return render(request, 'events/newsletter/list.html', {'newsletters': newsletters})


@login_required
def newsletter_detail(request, issue_number):
    newsletter = get_object_or_404(Newsletter, issue_number=issue_number, is_published=True)
    return render(request, 'events/newsletter/detail.html', {'newsletter': newsletter})


@permission_required('events.add_newsletter')
def newsletter_create(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            newsletter = form.save()
            messages.success(request, 'Newsletter created successfully!')
            return redirect('events:newsletter_detail', issue_number=newsletter.issue_number)
    else:
        form = NewsletterForm()
    return render(request, 'events/newsletter/create.html', {'form': form})


# Announcement Views
@login_required
def announcement_list(request):
    today = timezone.now().date()
    active_announcements = Announcement.objects.filter(
        is_active=True,
        start_date__lte=today,
        end_date__gte=today
    )
    return render(request, 'events/announcement/list.html', {
        'announcements': active_announcements
    })


@permission_required('coc.add_announcement')
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('events:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'events/announcement/create.html', {'form': form})


# Testimonial Video Views
@login_required
def testimonial_list(request):
    testimonials = TestimonialVideo.objects.filter(approved=True)
    featured = testimonials.filter(is_featured=True)[:6]
    recent = testimonials.filter(is_featured=False)[:12]
    return render(request, 'events/testimonial/list.html', {
        'featured_testimonials': featured,
        'recent_testimonials': recent
    })


@login_required
def testimonial_detail(request, slug):
    testimonial = get_object_or_404(TestimonialVideo, slug=slug, approved=True)
    testimonial.view_count += 1
    testimonial.save()
    return render(request, 'events/testimonial/detail.html', {'testimonial': testimonial})


@login_required
def testimonial_create(request):
    if request.method == 'POST':
        form = TestimonialVideoForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.uploaded_by = request.user
            testimonial.save()
            messages.success(request, 'Testimonial submitted for approval!')
            return redirect('events:testimonial_list')
    else:
        form = TestimonialVideoForm()
    return render(request, 'events/testimonial/create.html', {'form': form})


@login_required
def album_list(request):
    albums = PhotoAlbum.objects.filter(is_public=True)
    return render(request, 'events/gallery/album_list.html', {
        'albums': albums
    })


@login_required
def album_detail(request, slug):
    album = get_object_or_404(PhotoAlbum, slug=slug)
    photos = album.photos.all()

    return render(request, 'events/gallery/album_detail.html', {
        'album': album,
        'photos': photos
    })


@login_required
def create_album(request):
    if request.method == 'POST':
        form = PhotoAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.created_by = request.user
            album.save()
            messages.success(request, 'Album created successfully!')
            return redirect('events:album_detail', slug=album.slug)
    else:
        form = PhotoAlbumForm()

    return render(request, 'events/gallery/create_album.html', {'form': form})


@login_required
def upload_photos(request, album_slug):
    album = get_object_or_404(PhotoAlbum, slug=album_slug)

    if request.method == 'POST':
        form = MultiplePhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('images')
            for f in files:
                Photo.objects.create(
                    album=album,
                    image=f,
                    uploaded_by=request.user
                )
            messages.success(request, f'{len(files)} photos uploaded successfully!')
            return redirect('events:album_detail', slug=album.slug)
    else:
        form = MultiplePhotoUploadForm(initial={'album': album})

    return render(request, 'events/gallery/upload_photos.html', {
        'form': form,
        'album': album
    })


@login_required
def like_photo(request, photo_id):
    if request.is_ajax():
        photo = get_object_or_404(Photo, id=photo_id)
        if request.user in photo.likes.all():
            photo.likes.remove(request.user)
            liked = False
        else:
            photo.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'like_count': photo.like_count
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def video_list(request):
    categories = VideoCategory.objects.all()
    featured_videos = ArchivedVideo.objects.filter(is_featured=True)[:6]
    recent_videos = ArchivedVideo.objects.all()[:12]

    context = {
        'categories': categories,
        'featured_videos': featured_videos,
        'recent_videos': recent_videos,
    }
    return render(request, 'events/video_archive/list.html', context)


@login_required
def video_detail(request, slug):
    video = get_object_or_404(ArchivedVideo, slug=slug)
    video.view_count += 1
    video.save()

    related_videos = ArchivedVideo.objects.filter(
        Q(category=video.category) & ~Q(id=video.id)
    )[:4]

    return render(request, 'events/video_archive/detail.html', {
        'video': video,
        'related_videos': related_videos
    })


@login_required
def category_videos(request, slug):
    category = get_object_or_404(VideoCategory, slug=slug)
    videos = category.videos.all()

    return render(request, 'events/video_archive/category.html', {
        'category': category,
        'videos': videos
    })


@permission_required('events.add_archivedvideo')
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('events:video_detail', slug=video.slug)
    else:
        form = VideoUploadForm()

    return render(request, 'events/video_archive/upload.html', {'form': form})


@login_required
def search_videos(request):
    query = request.GET.get('q', '')
    if query:
        videos = ArchivedVideo.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        videos = ArchivedVideo.objects.none()

    return render(request, 'events/video_archive/search.html', {
        'videos': videos,
        'query': query
    })


def generate_stream_key():
    """Generate a unique stream key"""
    return str(uuid.uuid4())


@login_required
def create_stream(request):
    if request.method == 'POST':
        form = LiveStreamForm(request.POST, request.FILES)
        if form.is_valid():
            stream = form.save(commit=False)
            stream.created_by = request.user
            stream.stream_key = generate_stream_key()
            stream.save()

            # Add streaming information to context
            context = {
                'stream': stream,
                'rtmp_url': f"{settings.STREAM_RTMP_URL}{stream.stream_key}",
                'stream_url': f"{settings.STREAM_HLS_URL}{stream.stream_key}/index.m3u8",
            }
            return render(request, 'events/livestream/stream_info.html', context)
    else:
        form = LiveStreamForm()

    return render(request, 'events/livestream/create.html', {'form': form})


@login_required
def stream_list(request):
    upcoming_streams = LiveStream.objects.filter(
        scheduled_time__gte=timezone.now()
    ).order_by('scheduled_time')
    live_streams = LiveStream.objects.filter(is_live=True)

    return render(request, 'events/livestream/list.html', {
        'upcoming_streams': upcoming_streams,
        'live_streams': live_streams
    })


@login_required
def stream_detail(request, stream_id):
    stream = get_object_or_404(LiveStream, id=stream_id)
    chat_form = StreamChatForm()
    chats = stream.chats.all()[:100]  # Last 100 messages

    return render(request, 'events/livestream/detail.html', {
        'stream': stream,
        'chat_form': chat_form,
        'chats': chats
    })


@login_required
def create_stream(request):
    if request.method == 'POST':
        form = LiveStreamForm(request.POST, request.FILES)
        if form.is_valid():
            stream = form.save(commit=False)
            stream.created_by = request.user
            stream.stream_key = generate_stream_key()  # You'll need to implement this
            stream.save()
            return redirect('events:stream_detail', stream_id=stream.id)
    else:
        form = LiveStreamForm()

    return render(request, 'events/livestream/create.html', {'form': form})


@login_required
def post_chat(request, stream_id):
    if request.method == 'POST':
        stream = get_object_or_404(LiveStream, id=stream_id)
        form = StreamChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.stream = stream
            chat.user = request.user
            chat.save()
            return JsonResponse({
                'status': 'success',
                'message': chat.message,
                'user': chat.user.username,
                'timestamp': chat.timestamp.strftime('%H:%M')
            })
    return JsonResponse({'status': 'error'}, status=400)


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
    can_register = event.get_can_register(request.user)

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
    return render(request, 'outreach/missions/mission_list.html', {
        'active_missions': active_missions,
        'past_missions': past_missions
    })


@login_required
def edit_event(request, pk):
    """View for editing an existing event"""
    event = get_object_or_404(Event, pk=pk)

    # Check if user has permission to edit this event
    if request.user != event.creator and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('events:event_detail', pk=event.pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)
            # Any additional processing before saving
            updated_event.save()

            messages.success(request, f"Event '{event.title}' has been updated successfully.")
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
        'is_new': False,
    }
    return render(request, 'events/create_event.html', context)


@login_required
def delete_event(request, pk):
    """View for deleting an existing event"""
    event = get_object_or_404(Event, pk=pk)

    # Check if user has permission to delete this event
    if request.user != event.creator and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('events:event_detail', pk=event.pk)

    # Store the event title for the success message
    event_title = event.title

    if request.method == 'POST':
        # Actual deletion happens here
        event.delete()
        messages.success(request, f"Event '{event_title}' has been deleted successfully.")
        return redirect('events:events_list')

    # If it's a GET request, show the confirmation page
    context = {
        'event': event,
    }
    return render(request, 'events/event_confirm_delete.html', context)
