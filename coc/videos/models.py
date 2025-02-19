import logging
from accounts.models import User
from django.conf import settings
# from users.models import CustomUser
# from .utils import get_video_duration
# from like_system.models import LikesTarget
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from datetime import timedelta

logger = logging.getLogger(__name__)

CATEGORY_CHOICES = [
    ('SERMON', 'Sermon'),
    ('GOSPEL', 'Gospel'),
    ('PRAISE_AND_WORSHIP', 'Praise and Worship'),
    ('TESTIMONY', 'Testimony'),
    ('BIBLE_STUDY', 'Bible Study'),
    ('GENERAL', 'General'),
]

MODERATION_CHOICES = [
    ('PENDING', 'pending'),
    ('APPROVED', 'approved'),
    ('REJECTED', 'rejected'),
]

PRIVACY_CHOICES = [
        ('PUBLIC', 'public'),
        ('PRIVATE', 'private'),
        ('COMMUNITY', 'community'),
        ('MADE_FOR_KIDS', 'made_for_kids'),
    ]





class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Content(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='GENERAL')
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(default='static/imag/sa.jpg')
    audience = models.BooleanField(default=False)
    path = models.FileField(upload_to='videos/', null=True, verbose_name="")
    recording_date_and_location = models.DateTimeField(blank=True, null=True)
    language_and_captions_certification = models.BooleanField(default=False)
    license = models.BooleanField(default=False)
   # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    keywords = models.CharField(max_length=100, null=True, blank=True)

    views = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100, null=True, blank=True, choices=MODERATION_CHOICES, default='PENDING')
    privacy = models.CharField(max_length=100, choices=PRIVACY_CHOICES, default='PUBLIC')
    is_blocked = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)
    duration = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    promoted = models.BooleanField(default=False)
    url = models.URLField(default='https://example.com')


    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        # Use a more explicit check and ensure it returns a string always
        return self.title if self.title else "Content with No Title"

    def get_absolute_url(self):
        return reverse('videos:video_details', kwargs={'video_id': self.id})


class ShortVideo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)

    video_file = models.FileField(upload_to='short_videos/')
    thumbnail = models.ImageField(upload_to='short_video_thumbnails/', default='short_video.jpg')
    duration = models.DurationField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_shorts', blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_shorts', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()


class Moderation(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=MODERATION_CHOICES, )
    # video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()



class Privacy(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=100, choices=PRIVACY_CHOICES,)
    # video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.level



class ModerationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s request for {self.video.title}"


class ContentGuidelines(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


class LikedVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} liked {self.video.title}'


class FavoriteVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Content, on_delete=models.CASCADE)  # Assuming you have a Video model
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s  favorite videos:  {self.video.title}"




class UploadedVideo(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VideoView(models.Model):
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Share(models.Model):
    video = models.ForeignKey(Content, on_delete=models.CASCADE, blank=True, null=True)
    number_of_times_shared = models.PositiveIntegerField(default=0)
    shared = models.BooleanField(default=False)


class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(validators=[MinLengthValidator(150)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_comments')
    parent = models.ForeignKey('self', validators=[MinLengthValidator(150)], on_delete=models.CASCADE, blank=True, null=True)

    def get_total_likes(self):
        return self.likes.users.count()

    def total_dislikes(self):
        return self.dislikes.users.count()

    def __str__(self):
        return f'comment by {self.user} on {self.created_at}'[:30]

    class Meta:
        ordering = ['created_at']

class VideoLikes(models.Model):
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.video.title}"


class WatchedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_videos')
    video = models.ForeignKey(ShortVideo, on_delete=models.CASCADE, related_name='watched_by')
    watched_at = models.DateTimeField(auto_now_add=True)
    watch_duration = models.DurationField(null=True, blank=True)  # How long they watched
    completed = models.BooleanField(default=False)  # If they finished the video

    class Meta:
        ordering = ['-watched_at']
        unique_together = ['user', 'video']

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"


class LiveStreamEvent(models.Model):
    title = models.CharField(max_length=200)
    stream_key = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    description = models.TextField()


class WatchLater(models.Model):
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"


class Subscribe(models.Model):
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL)


class VideoQueue:
    def __init__(self):
        self.queue = []

    def add_video(self, video_id):
        """Add a video to the queue."""
        self.queue.append(video_id)
        print(f"Video {video_id} added to the queue.")

    def remove_video(self, video_id):
        """Remove a specific video from the queue."""
        if video_id in self.queue:
            self.queue.remove(video_id)
            print(f"Video {video_id} removed from the queue.")
        else:
            print(f"Video {video_id} not found in the queue.")

    def clear_queue(self):
        """Clear all videos from the queue."""
        self.queue.clear()
        print("All videos have been removed from the queue.")

    def display_queue(self):
        """Display the current queue."""
        print("Current Video Queue:")
        for idx, video_id in enumerate(self.queue, start=1):
            print(f"{idx}. Video ID: {video_id}")


class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queues')
    videos = models.ManyToManyField(Content, through='QueueItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Queue"

    @property
    def total_duration(self):
        return sum((video.duration for video in self.videos.all() if video.duration), timedelta())


class QueueItem(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position']
        unique_together = ['queue', 'position']


class Playlist(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', null=True)
    videos = models.ManyToManyField(Content, through='PlaylistVideo', related_name='in_playlists')
    thumbnail = models.ImageField(upload_to='playlist_thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def video_count(self):
        return self.videos.count()

    @property
    def total_duration(self):
        return sum((video.video.duration for video in self.videos.all() if video.video.duration), timedelta())


class PlaylistVideo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position']
        unique_together = ['playlist', 'position']


class DownloadedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloaded_videos')
    video = models.ForeignKey(Content, on_delete=models.CASCADE)
    local_path = models.CharField(max_length=255)  # Path where video is stored locally
    file_size = models.BigIntegerField()  # Size in bytes
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-downloaded_at']
        unique_together = ['user', 'video']

    def __str__(self):
        return f"{self.video.title} - {self.user.username}"

    def delete(self, *args, **kwargs):
        # Delete the local file when the record is deleted
        if os.path.exists(self.local_path):
            os.remove(self.local_path)
        super().delete(*args, **kwargs)


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    voice_search = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Search histories'
