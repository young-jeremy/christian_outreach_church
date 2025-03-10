import datetime
import json
import os
import tempfile
import threading
from datetime import datetime
from io import BytesIO

import cv2
import matplotlib.pyplot as plt
import pandas as pd
import speech_recognition as sr
from aiohttp.web_urldispatcher import View
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import default_storage
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from elasticsearch_dsl import Q
from firebase_admin import auth
from google.cloud import speech
from google.cloud import speech_v1 as speech
from google.cloud import vision
from google.cloud import vision, videointelligence
from moviepy.editor import VideoFileClip
from moviepy.editor import VideoFileClip
from requests import Request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import train_test_split

from accounts.forms import *
from accounts.signals import *
from comments.forms import CommentForm
from notifications.models import Notifications
from services.models import Channel, Subscription
from services.models import Sermon
from .firebase import initialize_firebase
from .forbidden_content import has_forbidden_content
from .forms import CategoryForm, ContentForm
from .forms import ContentModerationForm
from .forms import PlaylistForm, PlaylistVideoForm, PlaylistVideoForm
from .forms import VideoForm, VideoSearchForm, ModerationRequestForm, ShortVideoForm, \
    ContentSubmissionForm, CommentEditForm
from .models import *
from .models import Category
from .models import (
    Content, Comments, DownloadedVideo, Queue, QueueItem,
    Playlist, PlaylistVideo, ShortVideo, WatchedVideo
)
from .models import SearchHistory
from .models import WatchLater
from .utils import check_for_nudity
from .video_queue import VideoQueue


def search_videos(request):
    query = request.GET.get('q', '').strip()

    try:
        # Use basic Django query
        if query:
            videos = Content.objects.filter(
                status='APPROVED'
            ).filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(uploader__username__icontains=query)
            ).order_by('-created_at')
        else:
            videos = Content.objects.filter(status='APPROVED').order_by('-created_at')[:12]

        context = {
            'videos': videos,
            'query': query,
        }

        return render(request, 'videos/search_results.html', context)
    except Exception as e:
        print(f"Search error: {str(e)}")
        return render(request, 'videos/search_results.html', {
            'videos': [],
            'query': query,
            'error': 'An error occurred while searching.'
        })


def category_list(request):
    # Get all unique categories from the Content model
    categories = Content.objects.values_list('category', flat=True).distinct()

    # Fetch videos by category and status
    all_videos = Content.objects.all()
    all_gospel_videos = Content.objects.filter(category='GOSPEL')
    approved_videos = Content.objects.filter(status='APPROVED')
    rejected_videos = Content.objects.filter(status='REJECTED')

    # Get counts for different categories
    sermons = Content.objects.filter(category='SERMON').count()
    gospel_videos = Content.objects.filter(category='GOSPEL').count()
    praise_and_worship = Content.objects.filter(category='PRAISE_AND_WORSHIP').count()
    testimonies = Content.objects.filter(category='TESTIMONY').count()
    bible_studies = Content.objects.filter(category='BIBLE_STUDY').count()

    # Get latest videos for each category
    latest_sermons = Content.objects.filter(
        category='SERMON',
        status='APPROVED'
    ).order_by('-created_at')[:4]

    latest_gospel = Content.objects.filter(
        category='GOSPEL',
        status='APPROVED'
    ).order_by('-created_at')[:4]

    latest_worship = Content.objects.filter(
        category='PRAISE_AND_WORSHIP',
        status='APPROVED'
    ).order_by('-created_at')[:4]

    # Get trending/popular videos
    trending_videos = Content.objects.filter(
        status='APPROVED'
    ).order_by('-views')[:6]

    context = {
        'categories': categories,
        'all_videos': all_videos,
        'all_gospel_videos': all_gospel_videos,
        'approved_videos': approved_videos,
        'rejected_videos': rejected_videos,

        # Category counts
        'sermon_count': sermons,
        'gospel_count': gospel_videos,
        'worship_count': praise_and_worship,
        'testimony_count': testimonies,
        'bible_study_count': bible_studies,

        # Latest videos by category
        'latest_sermons': latest_sermons,
        'latest_gospel': latest_gospel,
        'latest_worship': latest_worship,

        # Trending videos
        'trending_videos': trending_videos,

        # Additional context
        'total_videos': all_videos.count(),
        'approved_count': approved_videos.count(),
        'rejected_count': rejected_videos.count(),
    }

    return render(request, 'dashboard/index.html', context)



@login_required
def offline_videos(request):
    # Get search and sort parameters
    search_query = request.GET.get('search', '')
    sort = request.GET.get('sort', '-downloaded_at')

    # Get downloaded videos
    downloaded = DownloadedVideo.objects.filter(user=request.user)

    # Apply search if provided
    if search_query:
        downloaded = downloaded.filter(
            Q(video__title__icontains=search_query) |
            Q(video__description__icontains=search_query)
        )

    # Apply sorting
    if sort in ['video__title', '-video__title', 'downloaded_at', '-downloaded_at', 'file_size', '-file_size']:
        downloaded = downloaded.order_by(sort)

    # Pagination
    paginator = Paginator(downloaded, 12)
    page = request.GET.get('page')
    downloaded_videos = paginator.get_page(page)

    context = {
        'downloaded_videos': downloaded_videos,
        'search_query': search_query,
        'sort': sort,
    }
    return render(request, 'videos/offline_videos.html', context)


@login_required
def play_offline_video(request, video_id):
    downloaded = get_object_or_404(DownloadedVideo, user=request.user, video_id=video_id)
    return render(request, 'videos/offline_player.html', {'downloaded': downloaded})


@login_required
def download_video(request, video_id):
    video = get_object_or_404(Content, id=video_id)

    # Check if already downloaded
    if DownloadedVideo.objects.filter(user=request.user, video=video).exists():
        messages.warning(request, 'Video already downloaded')
        return redirect('coc:video_details', video_id=video.id)

    try:
        # Create downloads directory if it doesn't exist
        download_dir = os.path.join(settings.MEDIA_ROOT, 'downloads', str(request.user.id))
        os.makedirs(download_dir, exist_ok=True)

        # Generate local path for the video
        filename = f"{video.id}_{slugify(video.title)}.mp4"
        local_path = os.path.join(download_dir, filename)

        # Copy video file to downloads directory
        with open(video.video_file.path, 'rb') as src, open(local_path, 'wb') as dst:
            dst.write(src.read())

        # Get file size
        file_size = os.path.getsize(local_path)

        # Create download record
        DownloadedVideo.objects.create(
            user=request.user,
            video=video,
            local_path=local_path,
            file_size=file_size
        )

        messages.success(request, 'Video downloaded successfully')
        return redirect('coc:offline_videos')

    except Exception as e:
        messages.error(request, f'Error downloading video: {str(e)}')
        return redirect('coc:video_details', video_id=video.id)


@login_required
def delete_downloaded_video(request, video_id):
    if request.method == 'POST':
        downloaded = get_object_or_404(DownloadedVideo, user=request.user, video_id=video_id)
        downloaded.delete()  # This will also delete the local file
        messages.success(request, 'Downloaded video deleted')
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def simple_plot(request):
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 25, 30.35]
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, marker='o')
    plt.title('simple line plot')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return HttpResponse(buffer, content_type='image/png')


# Testing VideoQueue functionality
video_queue = VideoQueue()

# Initialize Firebase
initialize_firebase()


@login_required
def my_videos(request):
    videos = Content.objects.filter(uploader=request.user).order_by('-created_at')

    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        videos = videos.filter(title__icontains=search_query)

    # Handle category filter
    category_id = request.GET.get('category')
    if category_id:
        videos = videos.filter(category_id=id)

    # Pagination
    paginator = Paginator(videos, 12)  # 12 videos per page
    page = request.GET.get('page')
    videos = paginator.get_page(page)

    # Get categories for filter
    categories = Category.objects.all()

    context = {
        'videos': videos,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
        'total_videos': videos.paginator.count if videos else 0,
    }

    return render(request, 'videos/my_videos.html', context)


@csrf_exempt
@login_required
def voice_search(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        # Save the audio file temporarily
        audio_file = request.FILES['audio']

        # Ensure temp directory exists
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_audio')
        os.makedirs(temp_dir, exist_ok=True)

        temp_path = os.path.join(temp_dir, f'temp_audio_{request.user.id}.wav')

        try:
            # Save the audio file
            with open(temp_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # Initialize recognizer
            recognizer = sr.Recognizer()

            # Load the audio file
            with sr.AudioFile(temp_path) as source:
                # Read the audio data
                audio_data = recognizer.record(source)

                # Attempt to recognize speech
                try:
                    query = recognizer.recognize_google(audio_data)

                    # Save to search history
                    SearchHistory.objects.create(
                        user=request.user,
                        query=query,
                        voice_search=True
                    )

                    return JsonResponse({
                        'success': True,
                        'query': query
                    })

                except sr.UnknownValueError:
                    return JsonResponse({
                        'success': False,
                        'error': 'Could not understand audio'
                    })
                except sr.RequestError as e:
                    return JsonResponse({
                        'success': False,
                        'error': f'Error with the speech recognition service: {str(e)}'
                    })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'An error occurred: {str(e)}'
            })

        finally:
            # Clean up - remove temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    })


def search_results(request):
    query = request.GET.get('query', '')
    results = []  # Perform your search logic here
    return render(request, 'search_results.html', {'query': query, 'results': results})


def search_for_videos(request):
    query = request.GET.get('q')
    results = SearchQuerySet().filter(content=query).load_all()
    return render(request, 'videos/video_search_results.html', {'results': results, 'query': query})


def my_data_view(request):
    # Create a sample DataFrame
    data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [24, 27, 22]}
    df = pd.DataFrame(data)

    # Convert DataFrame to HTML
    html_table = df.to_html()
    return HttpResponse(html_table)


def my_model_view(request):
    # Sample data for demonstration
    X = [[1], [2], [3], [4]]
    y = [1, 2, 3, 4]

    # Split data and train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LinearRegression().fit(X_train, y_train)

    # Predict and return result
    prediction = model.predict(X_test)
    return HttpResponse(f"Prediction: {prediction}")


def get_user_info(request):
    user = auth.get_user_by_email("user@example.com")
    print("User data:", user)
    return HttpResponse(f"User ID: {user.uid}")


def category_list(request):
    # Get all unique categories from the Content model
    categories = Content.objects.values_list('category', flat=True).distinct()

    # Fetch videos by category and status
    all_videos = Content.objects.all()
    all_gospel_videos = Content.objects.filter(category='GOSPEL')  # Use the exact category value
    approved_videos = Content.objects.filter(status='APPROVED')
    rejected_videos = Content.objects.filter(status='REJECTED')

    # Get counts for different categories
    sermons = Content.objects.filter(category='SERMON').count()
    gospel_videos = Content.objects.filter(category='GOSPEL').count()
    praise_and_worship = Content.objects.filter(category='PRAISE_AND_WORSHIP').count()
    testimonies = Content.objects.filter(category='TESTIMONY').count()
    bible_studies = Content.objects.filter(category='BIBLE_STUDY').count()

    # Get latest videos for each category
    latest_sermons = Content.objects.filter(category='SERMON', status='APPROVED').order_by('-created_at')[:4]
    latest_gospel = Content.objects.filter(category='GOSPEL', status='APPROVED').order_by('-created_at')[:4]
    latest_worship = Content.objects.filter(category='PRAISE_AND_WORSHIP', status='APPROVED').order_by('-created_at')[
                     :4]

    # Get trending/popular videos
    trending_videos = Content.objects.filter(status='APPROVED').order_by('-views')[:6]

    # Context to pass to the template
    context = {
        'categories': categories,
        'all_videos': all_videos,
        'all_gospel_videos': all_gospel_videos,
        'approved_videos': approved_videos,
        'rejected_videos': rejected_videos,

        # Category counts
        'sermon_count': sermons,
        'gospel_count': gospel_videos,
        'worship_count': praise_and_worship,
        'testimony_count': testimonies,
        'bible_study_count': bible_studies,

        # Latest videos by category
        'latest_sermons': latest_sermons,
        'latest_gospel': latest_gospel,
        'latest_worship': latest_worship,

        # Trending videos
        'trending_videos': trending_videos,

        # Additional context
        'total_videos': all_videos.count(),
        'approved_count': approved_videos.count(),
        'rejected_count': rejected_videos.count(),
    }

    return render(request, 'dashboard/index.html', context)

# List content by category
def content_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    contents = Content.objects.filter(category=category)
    return render(request, 'videos/content_by_category.html', {'category': category, 'contents': contents})


# Create new category
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('videos:category_list')
    else:
        form = CategoryForm()
    return render(request, 'videos/create_category.html', {'form': form})


# Create new content
def create_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('videos:category_list')
        Notifications.objects.create(
            user=request.user,
            message="Your video has been Published successfully!",
            notification_type="video"
        )

    else:
        form = ContentForm()
    return render(request, 'videos/create_content.html', {'form': form})


def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000


def detect_text_from_image(image_path):
    print(settings.credentials)  # Add this line to debug

    # Use credentials stored in settings.py
    client = vision.ImageAnnotatorClient(credentials=settings.credentials)

    # Load the image into memory
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image({'content': content})

    # Perform text detection
    response = client.text_detection(image=image)
    return response


def home_page(request):
    template_name = 'home/index.html'
    return render(request, template_name)

def home(request):
    template_name = 'home/three_column_homepage.html'
    all_gospel_videos = Content.objects.all()
    all_videos = Content.objects.all()
    approved_videos = Content.objects.filter(status='APPROVED')
    rejected_videos = Content.objects.filter(status='REJECTED')
    ads = Advertisement.objects.all()
    videos_per_page = 9
    paginator = Paginator(approved_videos, videos_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # path = video.path

    # form = VideoForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()

    context = {
        'approved_videos': approved_videos,
        'rejected_videos': rejected_videos,
        'ads': ads,
        'all_gospel_videos': all_gospel_videos,
    }
    return render(request, template_name, context)


def sermons(request):
    template_name = 'home/sermons.html'
    sermons_videos = Content.objects.filter(category='SERMON')
    return render(request, template_name, {'sermons_videos': sermons_videos})


def gospel_made_for_kids(request):
    template_name = 'home/gospel_made_for_kids.html'
    gospel_for_kids = Content.objects.filter(category='GOSPEL_MADE_FOR_KIDS')
    return render(request, template_name, {'gospel_for_kids': gospel_for_kids})


def praise_and_worship(request):
    template_name = 'home/praise_and_worship.html'
    praise_and_worship_videos = Content.objects.filter(category='PRAISE_AND_WORSHIP')
    return render(request, template_name, {'praise_and_worship_videos': praise_and_worship_videos})


def music(request):
    template_name = 'home/music_videos.html'
    music_videos = Content.objects.filter(category='MUSIC')
    return render(request, template_name, {'music_videos': music_videos})


def search(request):
    query = request.GET.get('q', '')
    results = SearchQuerySet().filter(content=query) if query else []
    return render(request, 'search/search.html', {'results': results, 'query': query})


def video_search(request):
    form = VideoSearchForm(request.GET or None)
    query = request.GET.get('query')
    results = []

    if query:
        # Use Q objects to search in title and description
        results = Content.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()  # Avoid duplicates in results if any

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'videos/video_search_results.html', context)



def channel_details(request, channel_id):
    template_name = 'videos/channel_details.html'
    channel = Channel.objects.get(pk=channel_id)
    user = request.user
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    account_subscriptions = Subscription.objects.filter(subscriber=request.user)
    videos_uploaded = Content.objects.filter(uploader=user)
    channels_subscribed = [subscription.channel for subscription in account_subscriptions]
    playlists = Playlist.objects.all()
    context = {
        'user_profile': user_profile,
        'account_subscriptions': account_subscriptions,
        'videos_uploaded': videos_uploaded,
        'channels_subscribed': channels_subscribed,
        'playlists': playlists

    }
    if request.method == 'POST':
        channel = Channel.objects.get(pk=channel_id)
        user = request.user
    else:
        channel = Channel.objects.create(pk=channel_id)
    return render(request, template_name, context)


def create_channel(request):
    template_name = 'videos/create_channel.html'
    form = ChannelForm()
    if request.user.is_authenticated:
        try:
            channel = request.user
        except Channel.DoesNotExist:
            channel = None
            if channel:
                messages.warning(request, "You already have a channel, Enjoy your Christian Content")
                return redirect('home:home')
            if request.method == 'POST':
                channel_name = request.POST('channel_name')
                new_channel = Channel(user=request.user, channel=channel_name)
                new_channel.save()
                messages.success(request,
                                 'New channel created successfully! You are now verified to upload on our site')
                return redirect('home:home')
            return render(request, template_name, )
    else:
        messages.error(request, "You need to be logged in in order to create a channel")
        return redirect('users:login')
    return render(request, template_name)


def channel_list(request):
    template_name = 'videos/channel_list.html'
    channels = Channel.objects.filter(owner=request.user)
    return render(request, template_name, {'channels': channels})


def admin_dashboard(request):
    videos = Content.objects.all()

    # path = video.path

    # form = VideoForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()

    context = {
        'videos': videos,
        # 'form': form,
    }
    return render(request, 'videos/your_videos.html', context)


def admin_panel(request):
    form = VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context = {

        'form': form,
    }
    return render(request, 'videos/admin_panel.html', context)


@login_required()
def upload_form(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            content_file = request.FILES['path']
            content = content_file.read().decode('utf-8')
            video = form.save(commit=False)
            is_nudity = check_for_nudity(video.video_content.read())
            if is_nudity:
                messages.error(request, 'The content contains nudity, Please upload another video')
            else:
                video.save()
                messages.success(request, 'Video uploaded successfully')
                return redirect('videos:category_list')

            if has_forbidden_content(content):
                # Content contains forbidden words or patterns
                return render(request, 'videos/upload.html', {'form': form,
                                                              'error_message': 'Content contains inappropriate words. Please review your content.'})

            # Save or process the content (e.g., save to the database)
            # ...

            return redirect('videos:upload_success')  # Redirect to a success page
    else:
        form = ContentForm()

    return render(request, 'videos/video_upload.html', {'form': form})


def upload_success(request):
    template_name = 'videos/upload_success'
    return render(request, template_name)


def recommended(request):
    template_name = 'videos/recommended.html'
    # Retrieve video data from the database
    recommended_videos = Content.objects.all()

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Combine video descriptions and categories to create a text field for each video
    video_texts = [f'{video.description} {video.category}' for video in recommended_videos]

    # Compute TF-IDF vectors for video descriptions and categories
    tfidf_matrix = tfidf_vectorizer.fit_transform(video_texts)

    # Calculate cosine similarity between user preferences and video TF-IDF vectors
    user_preferences = 'made_for_gospel praise_and_worship preachings'  # Replace with user's preferences
    user_preferences_vector = tfidf_vectorizer.transform([user_preferences])
    cosine_sim = linear_kernel(user_preferences_vector, tfidf_matrix)

    # Get the indices of videos sorted by similarity
    video_indices = cosine_sim[0].argsort()[::-1]

    # Recommend videos based on similarity
    recommended_videos = [recommended_videos[i] for i in video_indices]

    # Pass the recommended videos to the template
    context = {'recommended_videos': recommended_videos}
    return render(request, template_name, context)



def library(request):
    template_name = 'base_channel.html'
    user = request.user
    videos_uploaded = Content.objects.filter(owner=user)

    return render(request, template_name, {'videos_uploaded': videos_uploaded})


@login_required
def liked_videos(request):
    videos = Content.objects.filter(likes=request.user).order_by('-created_at')

    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        videos = videos.filter(title__icontains=search_query)

    # Handle category filter
    category_id = request.GET.get('category')
    if category_id:
        videos = videos.filter(category_id=category_id)

    # Pagination
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    videos = paginator.get_page(page)

    # Get categories for filter
    categories = Category.objects.all()

    context = {
        'videos': videos,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
        'total_likes': videos.paginator.count if videos else 0,
    }

    return render(request, 'videos/liked_videos.html', context)


def trending(request):
    template_name = 'videos/trending.html'
    return render(request, template_name)


@login_required()
def watch_later(request):
    template_name = 'videos/watch_later.html'
    watch_later_videos = Content.objects.filter(uploader=request.user)
    return render(request, template_name, {'watch_later_videos': watch_later_videos})


@login_required()
def add_watch_later(request, video_id):
    template_name = 'videos/add_to_watch_later.html'
    try:

        video = Content.objects.get(pk=video_id)

        # Create a WatchLater instance for the authenticated user and the selected video
        WatchLater.objects.create(user=request.user, video=video)

        return redirect('videos:watch_later')
    except Content.DoesNotExist:
        video = Content.objects.filter(pk=video_id)
        return render(request, template_name, {'video': video})


def remove_watch_later(request, watch_later_id):
    watch_later_video = Content.objects.filter(id=watch_later_id)
    watch_later_video.delete()
    return redirect('videos:watch_later')


def your_videos(request):
    template_name = 'videos/your_videos.html'
    return render(request, template_name)


def status(request, video_id):
    template_name = 'videos/status.html'
    video = Content.objects.filter(id=video_id)
    video_status = Content.objects.filter(video=video, status=video_id.status)
    return render(request, template_name, {'video_status': video_status})


def coming_events(request):
    template_name = 'videos/coming_events.html'
    return render(request, template_name)


def overview(request):
    template_name = 'videos/overview.html'
    return render(request, template_name)


def update_video_views(request, video_id):
    template_name = 'videos/video_details.html'
    video = Content.objects.get(pk=video_id)
    if request.method == 'POST':
        start_time = datetime.strptime(request.POST.get('start_time'), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(request.POST.get('end_time'), '%Y-%m-%d %H:%M:%S')
        duration_watched = (end_time - start_time).total_seconds()
        if duration_watched >= 30:
            video = Content.objects.get(pk=video_id)
            video.view_count += 1
            video.save()
            VideoView.objects.create(video=video, user=request.user)
            return JsonResponse({'message': 'View counted successfully'})
        return JsonResponse({'message': 'View not counted'})
    context = {
        'video': video

    }
    return render(request, template_name, context)


@login_required()
def dislike_video(request, video_id):
    template_name = 'videos/disliked_videos.html'
    video = get_object_or_404(Video, pk=video_id)
    dislike, created = Dislike.objects.get_or_create(user=request.user, video=video)

    if not created:
        dislike.delete()
        return redirect('videos:video_details', video_id=video_id)
    return render(request, template_name, {'video': video, 'dislike': dislike})


@login_required
def share_video(request, video_id):
    video = get_object_or_404(Content, pk=video_id)
    # Check if the user has already shared the video
    shared = Share.objects.filter(user=request.user, video=video).exists()

    if not shared:
        # Create a new share entry
        Share.objects.create(user=request.user, video=video)

    return redirect('videos:video_details', video_id=video_id)


def upload_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        if check_for_nudity(uploaded_image.url):
            return HttpResponse('Nudity detected. This content is not allowed.')
        else:
            # Process and save the image as acceptable content
            # ...
            return HttpResponse('Image uploaded successfully.')


def report_content(request, object_id):
    template_name = 'users/report_content.html'
    # content_type = ContentType.objects.get_for_id(content_type_id)
    # content_object = content_type.get_objects_for_this_type(id=object_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            Report.objects.create(
                user=request.user,
                # content_type=content_type,
                reason=reason,
                object_id=object_id,
            )
            return redirect('report_success')
        else:
            form = ReportForm()

        return render(request, template_name, {'form': form, })


@login_required
def post_comment(request, video_id, parent_id=None):
    # If parent_id is provided, this is a reply to a comment
    parent_comment = None
    if parent_id:
        parent_comment = get_object_or_404(Comments, id=parent_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Assign the current user as the commenter
            if parent_comment:
                comment.parent = parent_comment  # Set the parent if this is a reply
            comment.save()  # Save the comment
            return redirect('videos:video_details', comment.id)  # Redirect to the page showing the comment thread
    else:
        form = CommentForm()

    return render(request, 'videos/video_details.html', {'form': form, 'parent_comment': parent_comment})


@login_required
def post_detail(request, post_id):
    # Retrieve all comments for a specific post
    comments = Comments.objects.filter(parent__isnull=True, post_id=post_id)  # Root comments only
    return render(request, 'post_detail.html', {'comments': comments, 'post_id': post_id})


@login_required
def edit_comment(request, comment_id):
    template_name = 'videos/video_details.html'
    try:
        comment = Comments.objects.get(id=comment_id)
    except Comments.DoesNotExist:
        return HttpResponse('Comment not found ', status=404)
    if request.method == 'POST':
        form = CommentEditForm(request.POST)
        if comment.user == request.user:
            comment_text = request.POST.get('comment_text')
            comment.text = comment_text
            comment.save()
            return HttpResponse('Comment updated successfully')
        else:
            return redirect('videos:video_details', video_id=comment.video.pk)
    else:
        form = CommentEditForm()
        return render(request, template_name, {'form': form})


def like_comment(request, comment_id):
    template_name = 'videos/video_details.html'
    if request.method == 'POST':
        comment = Comments.objects.get(pk=comment_id)
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
        return JsonResponse({'likes_count': comment.likes.count()})
    else:
        comment = Comment.objects.get(pk=comment_id)
        return render(request, template_name, {'comment': comment})


@login_required
def delete_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Content, id=video_id, uploader=request.user)
        video.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def delete_comment(request, comment_id):
    template_name = 'videos/video_details.html'
    if request.method == 'POST':
        comment = get_object_or_404(Comments, pk=comment_id)
        # comment = Comment.objects.get(pk=comment_id)
        if comment.user == request.user:
            comment.delete()

        return redirect('videos:video_details', video_id=comment.video.pk)
    else:
        comment = get_object_or_404(Comments, pk=comment_id)
        return render(request, template_name, {'comment': comment})


def send_notifications(sender, recipient, interaction_type, video):
    content = f'{sender.username} {interaction_type} your video: {video.title}'
    notification = Notifications(user=recipient, video=video, content=content)
    notification.save()


def subscription_success(request):
    template_name = 'videos/subscriptions_success.html'
    return render(request, template_name)



def edit_video(request):
    template_name = 'videos/edit_video.html'
    video = Content.objects.filter()
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)


def submit_content(request):
    template_name = 'videos/content_submission.html'
    if request.method == 'POST':
        form = ContentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save()
            content.user = request.user
            content.save()
            ModerationRequest.objects.create(user=request.user, content=content)
            return redirect('videos:content_submission_success')
        else:
            form = ContentSubmissionForm()
            return render(request, template_name, {'form': form})


def blocked_videos(request, ):
    template_name = 'videos/blocked_videos.html'
    moderated_videos = Content.objects.filter(status__in=['REJECTED', 'BLOCKED'])
    return render(request, template_name, {'moderated_videos': moderated_videos})


def moderation_dashboard(request):
    template_name = 'videos/moderation_dashboard.html'
    if request.method == 'POST':
        form = ModerationRequestForm(request.POST)
        if request.user.is_staff:
            moderation_requests = ModerationRequest.objects.filter(is_approved=False)
            return HttpResponse({'moderation_requests': 'moderation_requests'})
        else:
            return redirect('videos:access_denied')
    else:
        form = ModerationRequestForm()
        moderation_requests = ModerationRequest.objects.filter(is_approved=False)
    return render(request, template_name, {'form': form, 'moderation_requests': moderation_requests})


def approve_content(request, video_id):
    if request.user.is_staff:
        content = get_object_or_404(Content, id=video_id)
        content.is_approved = True
        content.save()
        return redirect('videos:moderation_dashboard')
    else:
        return redirect('videos:access_denied')


def view_content_guidelines(request):
    template_name = 'videos/content_guidelines.html'
    guidelines = ContentGuidelines.objects.all()
    return render(request, template_name, {'guidelines': guidelines})


@login_required
@require_POST
def create_comment(request, video_id):
    video = get_object_or_404(Content, id=video_id)
    comment_text = request.POST.get('text', '')

    if not comment_text.strip():
        return JsonResponse({'error': 'Comment text cannot be empty.'}, status=400)

    # Save the comment
    comment = Comments.objects.create(video=video, user=request.user, text=comment_text)

    # You could also redirect to the video detail page after adding a comment
    return redirect('videos:video_details', video_id=video.id)


def video_details(request, video_id):
    video = get_object_or_404(Content, id=video_id)
    comments = Comments.objects.filter(video=video)

    # Get recommended videos (similar category, excluding current video)
    recommended_videos = Content.objects.filter(
        category=video.category
    ).exclude(id=video.id)[:5]  # Limit to 5 recommendations

    # Get profile pictures for comments
    for comment in comments:
        if hasattr(comment.user, 'socialaccount_set') and comment.user.socialaccount_set.exists():
            # Google account
            social_account = comment.user.socialaccount_set.first()
            comment.profile_picture = social_account.extra_data.get('picture')
        elif hasattr(comment.user, 'profile') and comment.user.profile.avatar:
            # Local account with custom avatar
            comment.profile_picture = comment.user.profile.avatar.url
        else:
            # Default avatar
            comment.profile_picture = '/static/images/default_avatar.png'  # Adjust path as needed

    # Get current user's profile picture
    user_profile_picture = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'socialaccount_set') and request.user.socialaccount_set.exists():
            social_account = request.user.socialaccount_set.first()
            user_profile_picture = social_account.extra_data.get('picture')
        elif hasattr(request.user, 'profile') and request.user.profile.avatar:
            user_profile_picture = request.user.profile.avatar.url
        else:
            user_profile_picture = 'static/img/undraw_profile_2.svg'  # Adjust path as needed

    # Handle time calculations
    video_upload_date = video.created_at
    if video_upload_date.tzinfo is not None:
        video_upload_date = video_upload_date.replace(tzinfo=None)

    current_time = timezone.now()
    if current_time.tzinfo is not None:
        current_time = current_time.replace(tzinfo=None)

    timesince_str = timesince(video_upload_date, current_time)
    main_unit = timesince_str.split(",")[0] if timesince_str else ""

    # Increment view count
    video.views += 1
    video.save()

    # Get queue items if user is authenticated
    queue_items = []
    is_in_queue = False
    if request.user.is_authenticated:
        queue, _ = Queue.objects.get_or_create(user=request.user)
        queue_items = QueueItem.objects.filter(queue=queue).select_related('video').order_by('position')
        is_in_queue = QueueItem.objects.filter(queue=queue, video=video).exists()

    context = {
        'video': video,
        'comments': comments,
        'main_unit': main_unit,
        'comment_form': CommentForm(),
        'queue_items': queue_items,
        'is_in_queue': is_in_queue,
        'recommended_videos': recommended_videos,

    }

    return render(request, 'videos/video_details.html', context)


def record_upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('videos:dashboard')  # Redirect to a list of uploaded videos
    else:
        form = VideoForm()

    return render(request, 'videos/record_video.html', {'form': form})


def favorite_videos(request):
    # Retrieve favorite videos for the current user
    user_profile = User.objects.filter(username=request.user)
    user_favorite_videos = UserProfile.objects.get(favorite_videos=request.user.username.favorite_videos)
    return render(request, 'videos/user_favorite_videos.html', {'user_favorite_videos': user_favorite_videos})


def upload_short_videos(request):
    template_name = 'videos/upload_short_videos.html'

    if request.method == 'POST':
        # Get the uploaded video file
        form = ShortVideoForm()
        uploaded_video = request.FILES.get('video')

        # Use a custom file upload handler to check video duration
        def handle_uploaded_file(f):
            media_type = f.content_type.split('/')[0]  # 'video' part of content type
            if media_type == 'video':
                duration = get_video_duration(f.temporary_file_path())
                if duration > max_duration:
                    return JsonResponse({'error': 'Video duration exceeds the limit.'})

        # Set the custom upload handler for the duration check
        request.upload_handlers = [TemporaryFileUploadHandler(request)]
        # Process the uploaded file with the custom handler
        uploaded_video = request.FILES.get('video')
        response = handle_uploaded_file(uploaded_video)

        if response:
            return response

        # Save the video to your media directory and store its path in the database
        # (You need to configure your media settings accordingly)
        # Example code to save the video:
        # video = VideoModel(video_file=uploaded_video)
        # video.save()

        # Check the video's duration and size
        max_duration = 60  # Maximum duration in seconds (1 minute)
        max_file_size = 20 * 1024 * 1024  # Maximum file size in bytes (20MB)

        if uploaded_video.size > max_file_size:
            return render(request, 'videos/video_error.html', )

        return JsonResponse({'success': 'Video uploaded successfully.'})
    form = ShortVideoForm()

    return render(request, template_name, {'form': form})


# Function to get video duration (you need to install the required library)
def get_video_duration(file_path):
    clip = VideoFileClip(file_path)
    return clip.duration


def short_videos(request):
    try:
        # Get all categories
        categories = Category.objects.all()
        results = []

        # Get current category filter and page from request
        current_category_id = request.GET.get('category')
        page_number = request.GET.get('page', 1)

        for category in categories:
            # Get videos for this category
            category_videos = ShortVideo.objects.filter(category=category)
            paginator = Paginator(category_videos, 6)  # 6 videos per page

            # Determine which page to show
            if current_category_id and int(current_category_id) == category.id:
                # Show requested page for selected category
                videos_page = paginator.get_page(page_number)
            else:
                # Show first page for other categories
                videos_page = paginator.get_page(1)

            # Create result object with category and its paginated videos
            results.append({
                'category': category,
                'videos': videos_page,
                'is_active': str(category.id) == current_category_id
            })

        context = {
            'categories': results,
            'current_category_id': current_category_id,
            'page_number': page_number
        }

        return render(request, 'videos/short_videos.html', context)

    except Exception as e:
        # Log the error and return empty categories
        print(f"Error in short_videos view: {str(e)}")
        return render(request, 'videos/short_videos.html', {'categories': []})


def notify_video_owner(video, user, liked):
    owner = video.user  # Assuming the video model has a ForeignKey to the user who uploaded it
    if liked:
        message = f"{user.username} liked your video: {video.title}"
    else:
        message = f"{user.username} unliked your video: {video.title}"
    messages.info(owner, message)


@login_required
def like_video(request, video_id):
    if request.method == 'POST':

        video = Content.objects.get(pk=video_id)
        user = request.user
        current_likes = video.likes
        liked = VideoLikes.objects.filter(user=user, video=video).count()
        if not liked:
            liked = VideoLikes.objects.create(video=video, user=user)
            current_likes += 1
        else:
            liked = VideoLikes.objects.create(video=video, user=request.user).delete()
            video = Content.objects.get(id=video_id)
            video.likes = current_likes
            video.save()
    video = Content.objects.get(id=video_id)
    return HttpResponseRedirect(reverse('videos:video_details', args=[video.id]), )


@login_required
def dislike_video(request, video_id):
    if request.method == 'POST':
        user = request.user
        video_id = request.POST.get('video_id')
        video = Video.objects.filter(video=video_id, user=user)
        try:
            video_like = VideoLikes.objects.get(user=user, video=video)
            video_like.delete()
            liked = False
        except VideoLikes.DoesNotExist:
            video_like = VideoLikes(user=user, video=video)
            video_like.save()
            liked = True

            notify_video_owner(Content, liked)
            return JsonResponse({'success': True, 'liked': liked})
        return JsonResponse({'success': False})


def record_short_videos(request):
    template_name = 'videos/record_short_videos.html'
    if request.method == 'POST':
        form = ShortVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request, 'videos:short_video_list')
    # Redirect to a page where the user can view the videos.
    else:
        form = ShortVideoForm()

    return render(request, template_name, {'form': form})


def video_traffic(request, video_id):
    video = get_object_or_404(Content, id=video_id)
    # Assuming you have fields like 'views', 'likes', 'shares', 'comments' in your Video model
    views = video.views
    likes = LikedVideo.objects.filter(video=video)
    # shares = video.shares
    comments = video.comments

    return render(request, 'videos/video_traffic.html', {
        'video': video,
        'views': views,
        'likes': likes,
        # 'shares': shares,
        'comments': comments,
    })


def privacy_policy(request):
    template_name = 'home/privacy_policy.html'
    return render(request, template_name)


def public_terms_of_service(request):
    template_name = 'home/public_terms_of_service.html'
    return render(request, template_name)


def moderate_content(request, video_id, instance):
    video = Content.objects.get(pk=video_id)
    status = Privacy.objects.filter(status=Privacy.status)

    if request.method == 'POST':
        form = ContentModerationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('videos:videos')  # Redirect to the list of content
    else:
        form = ContentModerationForm()

    return render(request, 'privacy/moderate_content.html', {'form': form, 'video': video, 'status': status})


def short_video_details(request, video_id):
    video = get_object_or_404(ShortVideo, id=video_id)
    video.views += 1
    video.save()

    related_videos = ShortVideo.objects.filter(
        category=video.category
    ).exclude(id=video.id)[:6]

    # Add debug information
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"Username: {request.user.username}")

    context = {
        'video': video,
        'related_videos': related_videos,
        'user': request.user,  # Explicitly add user to context
    }
    return render(request, 'videos/short_video_details.html', context)


@login_required
def like_short_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(ShortVideo, id=video_id)
        like, created = ShortVideoLike.objects.get_or_create(
            user=request.user,
            video=video
        )

        if not created:
            # User already liked, so unlike
            like.delete()
            liked = False
        else:
            # New like
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': video.likes_count
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def blocked_video_details(request, video_id):
    template_name = 'videos/blocked_video_details.html'
    video = Content.objects.filter(pk=video_id)
    rejected_videos = Content.objects.filter(status='rejected')
    return render(request, template_name, {'rejected_videos': rejected_videos})


def approved_videos(request):
    template_name = 'videos/approved_videos.html'
    approved_content = Content.objects.filter(is_approved=True)
    return render(request, template_name, {'approved_content': approved_content})


def pending_videos(request):
    template_name = 'videos/pending_videos.html'
    total_pending_videos = Video.objects.filter(status='PENDING')
    return render(request, template_name, {'total_pending_videos': total_pending_videos})


@login_required
def playlist_list(request):
    # Get search parameter
    search_query = request.GET.get('search', '')

    # Get user's playlists
    playlists = Playlist.objects.filter(creator=request.user)

    # Apply search if provided
    if search_query:
        playlists = playlists.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Get total count before pagination
    total_playlists = playlists.count()

    # Pagination
    paginator = Paginator(playlists, 12)
    page = request.GET.get('page')
    playlists = paginator.get_page(page)

    # Add video count to each playlist
    for playlist in playlists:
        video_count = playlist.videos

    context = {
        'playlists': playlists,
        'total_playlists': total_playlists,
        'search_query': search_query,
    }
    return render(request, 'videos/playlist/playlist_list.html', context)


@login_required
def playlist_detail(request, slug):
    playlist = get_object_or_404(Playlist, slug=slug)
    videos = playlist.playlist_videos.select_related('video').order_by('position')

    # Add video count
    playlist.video_count = videos.count()

    context = {
        'playlist': playlist,
        'videos': videos,
        'is_owner': request.user == playlist.creator
    }
    return render(request, 'videos/playlist/playlist_detail.html', context)


@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.creator = request.user
            playlist.save()
            messages.success(request, 'Playlist created successfully!')
            return redirect('coc:playlist_detail', slug=playlist.slug)
    else:
        form = PlaylistForm()

    return render(request, 'videos/playlist/create_playlist.html', {'form': form})


@login_required
def playlist_detail(request, slug):
    playlist = get_object_or_404(Playlist, slug=slug)
    videos = PlaylistVideo.objects.filter(playlist=playlist).select_related('video').order_by('position')

    if request.method == 'POST':
        form = PlaylistVideoForm(request.POST)
        if form.is_valid():
            video_id = request.POST.get('video_id')
            position = form.cleaned_data['position']
            video = get_object_or_404(ShortVideo, id=video_id)

            # Get the highest position number
            max_position = PlaylistVideo.objects.filter(playlist=playlist).aggregate(
                Max('position'))['position__max'] or 0

            PlaylistVideo.objects.create(
                playlist=playlist,
                video=video,
                position=max_position + 1
            )
            messages.success(request, 'Video added to playlist!')
            return redirect('videos:playlist_detail', slug=slug)

    context = {
        'playlist': playlist,
        'videos': videos,
    }
    return render(request, 'videos/playlist/playlist_detail.html', context)


@login_required
def add_to_playlist(request, slug, video_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)
        video = get_object_or_404(ShortVideo, id=video_id)

        # Get the highest position number
        max_position = PlaylistVideo.objects.filter(playlist=playlist).aggregate(
            Max('position'))['position__max'] or 0

        PlaylistVideo.objects.create(
            playlist=playlist,
            video=video,
            position=max_position + 1
        )

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def reorder_playlist(request, slug):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)
        video_ids = json.loads(request.body).get('video_ids', [])

        # Update positions
        with transaction.atomic():
            for index, video_id in enumerate(video_ids, start=1):
                PlaylistVideo.objects.filter(
                    playlist=playlist,
                    video_id=video_id
                ).update(position=index)

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.creator = request.user
            playlist.save()
            messages.success(request, 'Playlist created successfully!')
            return redirect('videos:playlist_detail', slug=playlist.slug)
    else:
        form = PlaylistForm()

    return render(request, 'videos/playlist/create_playlist.html', {'form': form})


@login_required
def delete_playlist(request, slug):
    playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)

    if request.method == 'POST':
        try:
            playlist.delete()
            messages.success(request, 'Playlist deleted successfully.')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'Error deleting playlist: {str(e)}')
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def remove_video_from_playlist(request, slug, video_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)
        playlist.videos.remove(video_id)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def moderation_request(request):
    template_name = 'videos/moderation_requests.html'
    moderation_requests = ModerationRequest.objects.filter(is_approved=False)
    if request.method == 'POST':
        form = ModerationRequestForm(request.POST)
        if request.user.is_staff:
            moderation_requests = ModerationRequest.objects.filter(is_approved=False)
            return HttpResponse({'moderation_requests': 'moderation_requests'})
        else:
            return redirect('videos:access_denied')
    else:
        form = ModerationRequestForm()
        moderation_requests = ModerationRequest.objects.filter(is_approved=False)
    return render(request, template_name, {'moderation_requests': moderation_requests, 'form': form})


@login_required
def add_to_favorites(request, video_id):
    video = get_object_or_404(Content, pk=video_id)

    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Check if the video is not already in favorites to avoid duplicates
    if video not in user_profile.favorite_videos.all():
        user_profile.favorite_videos.add(video)
        user_profile.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'already_added'})


@login_required
def watched_videos(request):
    watched = WatchedVideo.objects.filter(user=request.user).select_related('video')

    # Filter options
    filter_type = request.GET.get('filter')
    if filter_type == 'completed':
        watched = watched.filter(completed=True)
    elif filter_type == 'in_progress':
        watched = watched.filter(completed=False)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        watched = watched.filter(video__title__icontains=search_query)

    # Sorting
    sort = request.GET.get('sort', '-watched_at')
    watched = watched.order_by(sort)

    # Pagination
    paginator = Paginator(watched, 12)
    page = request.GET.get('page')
    watched = paginator.get_page(page)

    context = {
        'watched_videos': watched,
        'filter_type': filter_type,
        'search_query': search_query,
        'sort': sort,
    }
    return render(request, 'videos/watched_videos.html', context)


@login_required
def mark_video_watched(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(ShortVideo, id=video_id)
        watch_duration = request.POST.get('duration')
        completed = request.POST.get('completed', False)

        watched, created = WatchedVideo.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={
                'watch_duration': watch_duration,
                'completed': completed
            }
        )

        if not created:
            watched.watch_duration = watch_duration
            watched.completed = completed
            watched.save()

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def queue_view(request):
    # Get or create user's queue
    queue, created = Queue.objects.get_or_create(user=request.user)
    queue_items = QueueItem.objects.filter(queue=queue).select_related('video').order_by('position')

    context = {
        'queue': queue,
        'queue_items': queue_items,
    }
    return render(request, 'videos/queue.html', context)


@login_required
def add_to_queue(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(ShortVideo, id=video_id)
        queue, created = Queue.objects.get_or_create(user=request.user)

        # Get the highest position
        max_position = QueueItem.objects.filter(queue=queue).aggregate(
            Max('position'))['position__max'] or 0

        # Add to queue
        QueueItem.objects.create(
            queue=queue,
            video=video,
            position=max_position + 1
        )

        messages.success(request, 'Video added to queue!')
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def remove_from_queue(request, video_id):
    if request.method == 'POST':
        queue = get_object_or_404(Queue, user=request.user)
        QueueItem.objects.filter(queue=queue, video_id=video_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def reorder_queue(request):
    if request.method == 'POST':
        queue = get_object_or_404(Queue, user=request.user)
        video_ids = json.loads(request.body).get('video_ids', [])

        with transaction.atomic():
            for index, video_id in enumerate(video_ids, start=1):
                QueueItem.objects.filter(
                    queue=queue,
                    video_id=video_id
                ).update(position=index)

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def live_stream(request):
    # In a real-world scenario, you would fetch the live stream URL or embed code here.
    template_name = 'videos/stream.html'
    live_stream_url = "YOUR_LIVE_STREAM_URL"  # Replace with your live stream URL

    return render(request, template_name, {'live_stream_url': live_stream_url})


class VideoCamera(object):
    def __int__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobtes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def camera_home(request):
    template_name = 'videos/video_camera.html'
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace;boundary=frame')
    except:
        pass
    return render(request, template_name)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'r\n\r\n'
        )


def all_videos(request):
    template_name = 'videos/three-column.html'
    all_gospel_videos = Content.objects.all()
    return render(request, template_name, {'all_gospel_videos': all_gospel_videos})


def live_videos(request):
    template_name = 'videos/live_videos.html'
    return render(request, template_name)


def generate_captions(request):
    template_name = 'videos/generate_captions.html'
    if request.method == 'POST':
        video = request.FILES['video']
        client = speech.SpeechClient()

        with video.open('rb') as video_file:
            content = video_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                          sample_rate_hertz=16000, language_code="en-US", )

        response = client.recognize(config=config, audio=audio)

        captions = [result.alternatives[0].transcript for result in response.results]

        return render(request, 'captions.html', {'captions': captions})

    return render(request, template_name)


class Requirement(View):
    form_class = CommentForm
    template_name = 'ktu/comment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        comment = Comments.objects.all()
        context = {'page_obj': comment, 'form': form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.user = request.user
            comment_form.save()
            messages.success(request, 'Your comment successfully addedd')

            return HttpResponseRedirect(reverse('comment'))

        context = {'form': form}

        return render(request, self.template_name, context)

    @classmethod
    def as_view(cls):
        pass


class UpdateCommentVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def __init__(self, request: Request):
        super().__init__(request)
        self.kwargs = None

    def get(self, request, *args, **kwargs):

        comment_id = self.kwargs.get('comment_id', None)
        opinion = self.kwargs.get('opinion', None)

        comment = get_object_or_404(Comments, id=comment_id)

        try:
            comment.dis_likes
        except Comment.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(comment=comment)

        try:
            comment.likes
        except Comments.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(comment=comment)

        if opinion.lower() == 'like':

            if request.user in comment.likes.users.all():
                comment.likes.users.remove(request.user)
            else:
                comment.likes.users.add(request.user)
                comment.dis_likes.users.remove(request.user)

        elif opinion.lower() == 'dis_like':

            if request.user in comment.dis_likes.users.all():
                comment.dis_likes.users.remove(request.user)
            else:
                comment.dis_likes.users.add(request.user)
                comment.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('comment'))
        return HttpResponseRedirect(reverse('comment'))

    @classmethod
    def as_view(cls):
        pass


def reply_comment(request):
    template_name = 'videos/video_details.html'
    return render(request, template_name, )


def add_subscriptions(request, id):
    sub = Subscribe.objects.get(id=id)
    sub_list = list(sub.subscriber.values())
    return JsonResponse(sub_list, safe=False, status=200)


def subscription_load(request, id):
    subscribers = Subscribe.objects.get(id=id)
    user = request.user
    if user in subscribers.subscriber.all():
        subscribers.subscriber.remove(user)
        response = 'Subscribe'
        return JsonResponse(response, safe=False, status=200)
    else:
        subscribers.subscriber.add(user)
        response = 'Unsubscribe'
        return JsonResponse(response, safe=False, status=200)


def testimonies(request):
    template_name = 'home/testimonies.html'
    all_testimonies = Content.objects.filter(category='ALL_TESTIMONIES')
    return render(request, template_name, {'all_testimonies': all_testimonies})


def evangelism(request):
    template_name = 'home/evangelism.html'
    evangelism_videos = Content.objects.filter(category='EVANGELISM')
    return render(request, template_name, {'evangelism_videos': evangelism_videos})


def bible_discussions(request):
    bible_discussion_videos = Content.objects.filter(category='BIBLE_DISCUSSIONS')
    paginator = Paginator(bible_discussion_videos, 9)
    page = request.GET.get('page')
    bible_discussion_videos = paginator.get_page(page)
    return render(request, template_name, {'bible_discussion_videos': bible_discussion_videos})


def add_video_to_queue(request, video_id):
    video_queue.add_video(video_id)
    return JsonResponse({"message": f"Video {video_id} added to queue", "queue": video_queue.display_queue()})


def remove_video_from_queue(request, video_id):
    video_queue.remove_video(video_id)
    return JsonResponse({"message": f"Video {video_id} removed from queue", "queue": video_queue.display_queue()})


def clear_video_queue(request):
    video_queue.clear_queue()
    return JsonResponse({"message": "Video queue cleared", "queue": video_queue.display_queue()})


def display_video_queue(request):
    queue = video_queue.display_queue()
    return render(request, 'videos/video_details.html', {'queue': video_queue.display_queue()})


@login_required
def user_uploaded_videos(request):
    # Get all videos uploaded by the current user
    uploaded_videos = Content.objects.filter(uploader=request.user)

    # Render the template and pass the list of videos
    return render(request, 'videos/your_videos.html', {'uploaded_videos': uploaded_videos})



def sermon_detail(request, video_id):
    sermon = get_object_or_404(Sermon, id=video_id)

    # Get related sermons
    related_sermons = Sermon.objects.filter(preacher=request.user).exclude(id=video_id).order_by('-created_at')[:4]

    # Handle comments
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.video = sermon
            comment.save()
            return redirect('videos:sermon_detail', video_id=sermon.id)
    else:
        comment_form = CommentForm()

    # Get comments for this sermon
    comments = Comments.objects.filter(id=video_id).order_by('-created_at')

    # Increment view count
    sermon.views += 1
    sermon.save()

    context = {
        'sermon': sermon,
        'related_sermons': related_sermons,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'videos/sermons/sermon_detail.html', context)



@login_required
def add_video_comment(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Content, id=video_id)  # Using Content instead of Video
        content = request.POST.get('content')
        if content:
            Comments.objects.create(  # Using Comments instead of VideoComment
                video=video,
                user=request.user,
                content=content
            )
            messages.success(request, 'Comment added successfully!')
        return redirect('videos:video_details', video_id=video.id)
    return redirect('videos:video_details', video_id=video_id)


class VideoProcessingMixin:
    def process_video(self, video_file):
        """Process video file for inappropriate content and extract metadata"""
        results = {
            'duration': 0,
            'has_inappropriate_content': False,
            'captions': [],
            'thumbnail': None
        }

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video:
            for chunk in video_file.chunks():
                temp_video.write(chunk)
            temp_video_path = temp_video.name

        try:
            # Get video metadata
            with VideoFileClip(temp_video_path) as clip:
                results['duration'] = clip.duration

                # Generate thumbnail
                thumbnail_time = min(5, clip.duration / 2)  # Get frame at 5 seconds or video midpoint
                thumbnail = clip.get_frame(thumbnail_time)
                results['thumbnail'] = self.save_thumbnail(thumbnail)

                # Extract audio for speech-to-text
                audio_path = self.extract_audio(clip)
                results['captions'] = self.generate_captions(audio_path)

            # Check for inappropriate content
            results['has_inappropriate_content'] = self.check_inappropriate_content(temp_video_path)

        finally:
            # Cleanup temporary files
            os.unlink(temp_video_path)
            if 'audio_path' in locals():
                os.unlink(audio_path)

        return results

    def extract_audio(self, clip):
        """Extract audio from video for speech recognition"""
        audio_path = tempfile.mktemp(suffix='.wav')
        clip.audio.write_audiofile(audio_path)
        return audio_path

    def generate_captions(self, audio_path):
        """Generate captions from audio using speech recognition"""
        recognizer = sr.Recognizer()
        captions = []

        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                captions.append({
                    'text': text,
                    'start': 0,
                    'end': 0  # You might want to implement proper timing
                })
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Speech Recognition service; {e}")

        return captions

    def check_profanity(self, captions):
        """Check for profanity in captions"""
        text = ' '.join(caption['text'] for caption in captions)
        return predict_prob([text])[0] > 0.5

    def check_inappropriate_content(self, video_path):
        """Check for inappropriate content using Google Cloud Video Intelligence"""
        client = videointelligence.VideoIntelligenceServiceClient(credentials=settings.credentials)

        with open(video_path, 'rb') as file:
            input_content = file.read()

        features = [
            videointelligence.Feature.EXPLICIT_CONTENT_DETECTION,
        ]

        operation = client.annotate_video(
            request={
                "features": features,
                "input_content": input_content,
            }
        )

        result = operation.result(timeout=90)

        # Check if any frame has inappropriate content
        for frame in result.annotation_results[0].explicit_annotation.frames:
            if frame.pornography_likelihood >= videointelligence.Likelihood.LIKELY:
                return True

        return False

    def save_thumbnail(self, frame):
        """Save video thumbnail"""
        thumbnail_path = tempfile.mktemp(suffix='.jpg')
        frame.save(thumbnail_path)

        # Save to Django storage
        with open(thumbnail_path, 'rb') as f:
            stored_path = default_storage.save(
                f'video_thumbnails/{os.path.basename(thumbnail_path)}',
                f
            )

        os.unlink(thumbnail_path)
        return stored_path


def create_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user

            # Process video
            processor = VideoProcessingMixin()
            results = processor.process_video(request.FILES['video'])

            # Check for inappropriate content
            if results['has_inappropriate_content']:
                messages.error(request, 'Video contains inappropriate content and cannot be uploaded.')
                return render(request, 'videos/video_checks/video_upload.html', {'form': form})

            # Save video with processed data
            video.duration = results['duration']
            video.thumbnail = results['thumbnail']
            video.captions = results['captions']
            video.save()

            # Create notification
            Notifications.objects.create(
                user=request.user,
                message="Your video has been published successfully!",
                notification_type="video",
                content_object=video
            )

            messages.success(request, 'Video uploaded successfully!')
            return redirect('videos:video_detail', pk=video.pk)
    else:
        form = VideoForm()

    return render(request, 'videos/video_checks/video_upload.html', {'form': form})


class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_checks/video_list.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Video.objects.filter(is_active=True)
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort', 'recent')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        if category:
            queryset = queryset.filter(category=category)

        if sort == 'popular':
            queryset = queryset.order_by('-view_count')
        elif sort == 'liked':
            queryset = queryset.order_by('-like_count')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Video.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        context['sort'] = self.request.GET.get('sort', 'recent')
        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_checks/video_details.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['related_videos'] = Video.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:6]
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        self.object.view_count += 1
        self.object.save()
        return response


class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    template_name = 'videos/video_checks/video_form.html'
    fields = ['title', 'description', 'video_file', 'thumbnail', 'is_active']

    def get_success_url(self):
        return reverse_lazy('videos:video_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        # Only allow editing of videos uploaded by the current user
        return Video.objects.filter(user=self.request.user)


class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'videos/video_checks/video_confirm_delete.html'
    success_url = reverse_lazy('videos:video_list')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.user


def video_like(request, slug):
    if request.method == 'POST' and request.is_ajax():
        video = get_object_or_404(Video, slug=slug)
        if request.user in video.likes.all():
            video.likes.remove(request.user)
            liked = False
        else:
            video.likes.add(request.user)
            liked = True
        return JsonResponse({
            'liked': liked,
            'like_count': video.likes.count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_comment(request, slug):
    if request.method == 'POST':
        video = get_object_or_404(Video, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return JsonResponse({
                'success': True,
                'comment_html': render_to_string('videos/video_checks/comment.html',
                                                 {'comment': comment}, request=request)
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def check_processing_status(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return JsonResponse({
        'status': video.processing_status,
        'progress': video.processing_progress
    })
