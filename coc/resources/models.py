from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from accounts.models import *


class DownloadableResource(models.Model):
    RESOURCE_TYPES = [
        ('PDF', 'PDF Document'),
        ('DOC', 'Word Document'),
        ('PPT', 'PowerPoint'),
        ('XLS', 'Excel Spreadsheet'),
        ('ZIP', 'ZIP Archive'),
        ('IMG', 'Image'),
        ('VID', 'Video'),
        ('AUD', 'Audio'),
    ]

    CATEGORIES = [
        ('BIB', 'Bible Study'),
        ('SER', 'Sermon Notes'),
        ('WOR', 'Worship Resources'),
        ('CHI', 'Children Ministry'),
        ('YTH', 'Youth Ministry'),
        ('EVA', 'Evangelism'),
        ('DIS', 'Discipleship'),
        ('LEA', 'Leadership'),
        ('PRA', 'Prayer'),
        ('OTH', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='downloads/')
    thumbnail = models.ImageField(upload_to='downloads/thumbnails/', blank=True, null=True)
    resource_type = models.CharField(max_length=3, choices=RESOURCE_TYPES)
    category = models.CharField(max_length=3, choices=CATEGORIES)
    author = models.CharField(max_length=100)
    version = models.CharField(max_length=20, blank=True)

    # File metadata
    file_size = models.BigIntegerField(editable=False, null=True)
    file_type = models.CharField(max_length=50, editable=False)

    # Access control
    is_public = models.BooleanField(default=True)
    requires_login = models.BooleanField(default=False)
    allowed_groups = models.ManyToManyField('auth.Group', blank=True)

    # Analytics
    download_count = models.IntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True, blank=True)

    # Organization
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    featured = models.BooleanField(default=False)

    # Timestamps
    upload_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Downloadable Resource'
        verbose_name_plural = 'Downloadable Resources'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)

    def get_download_url(self):
        return reverse('resources:download_file', args=[str(self.id)])

    def increment_downloads(self):
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save()

    def can_user_download(self, user):
        if self.is_public and not self.requires_login:
            return True
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        if self.allowed_groups.exists():
            return user.groups.filter(id__in=self.allowed_groups.all()).exists()
        return self.requires_login


class Podcast(models.Model):
    PODCAST_CATEGORIES = [
        ('SER', 'Sermons'),
        ('BIB', 'Bible Study'),
        ('DEV', 'Devotional'),
        ('YOU', 'Youth'),
        ('WOR', 'Worship'),
        ('LEA', 'Leadership'),
        ('EVA', 'Evangelism'),
        ('TES', 'Testimonies'),
    ]

    title = models.CharField(max_length=200)
    host = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=3, choices=PODCAST_CATEGORIES)
    cover_image = models.ImageField(upload_to='podcasts/covers/', help_text="Square image recommended (1400x1400px)")
    audio_file = models.FileField(upload_to='podcasts/audio/')
    duration = models.DurationField(help_text="Duration in HH:MM:SS format")
    publish_date = models.DateTimeField()
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    # RSS Feed and SEO fields
    subtitle = models.CharField(max_length=255, blank=True)
    keywords = models.CharField(max_length=500, help_text="Comma-separated keywords")
    explicit_content = models.BooleanField(default=False)

    # Analytics fields
    play_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    # Technical fields
    audio_type = models.CharField(max_length=50, default='audio/mpeg')
    file_size = models.BigIntegerField(help_text="File size in bytes", null=True, blank=True)

    # Transcript and accessibility
    transcript = models.TextField(blank=True)
    show_notes = models.TextField(blank=True)

    # Social sharing
    share_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date']
        verbose_name = 'Podcast Episode'
        verbose_name_plural = 'Podcast Episodes'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('resources:podcast_detail', args=[str(self.id)])

    def increment_play_count(self):
        self.play_count += 1
        self.save()

    def increment_download_count(self):
        self.download_count += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.file_size and self.audio_file:
            self.file_size = self.audio_file.size
        super().save(*args, **kwargs)


class TeachingResource(models.Model):
    RESOURCE_TYPES = [
        ('PDF', 'PDF Document'),
        ('DOC', 'Word Document'),
        ('PPT', 'PowerPoint'),
        ('VID', 'Video'),
        ('AUD', 'Audio'),
        ('WEB', 'Web Resource'),
    ]

    CATEGORIES = [
        ('BIB', 'Bible Study'),
        ('THE', 'Theology'),
        ('DIS', 'Discipleship'),
        ('EVA', 'Evangelism'),
        ('LEA', 'Leadership'),
        ('YOU', 'Youth Ministry'),
        ('CHI', 'Children Ministry'),
        ('WOR', 'Worship'),
        ('OTH', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=3, choices=RESOURCE_TYPES)
    category = models.CharField(max_length=3, choices=CATEGORIES)
    file = models.FileField(upload_to='teaching_resources/', null=True, blank=True)
    external_link = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Teaching Resource'
        verbose_name_plural = 'Teaching Resources'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('resources:teaching_resource_detail', args=[str(self.id)])

    def increment_downloads(self):
        self.download_count += 1
        self.save()


class SermonNotes(models.Model):
    SERMON_CATEGORIES = [
        ('SUN', 'Sunday Service'),
        ('MID', 'Midweek Service'),
        ('SPE', 'Special Service'),
        ('YTH', 'Youth Service'),
        ('CON', 'Conference'),
        ('REV', 'Revival'),
    ]

    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100)
    date_preached = models.DateField()
    bible_reference = models.CharField(max_length=200)
    category = models.CharField(max_length=3, choices=SERMON_CATEGORIES)
    main_points = models.TextField(help_text="Enter the main points of the sermon")
    key_scriptures = models.TextField(help_text="Enter key scripture references")
    summary = models.TextField()
    application_points = models.TextField(help_text="Practical application points from the sermon")
    additional_notes = models.TextField(blank=True)
    audio_recording = models.FileField(upload_to='sermon_recordings/', blank=True, null=True)
    slides = models.FileField(upload_to='sermon_slides/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_preached']
        verbose_name = 'Sermon Note'
        verbose_name_plural = 'Sermon Notes'

    def __str__(self):
        return f"{self.title} - {self.preacher} ({self.date_preached})"


class ReviewableMixin(models.Model):
    reviews = GenericRelation('Review')

    class Meta:
        abstract = True

    @property
    def average_rating(self):
        ratings = self.reviews.values_list('rating', flat=True)
        return sum(ratings) / len(ratings) if ratings else 0

    @property
    def review_count(self):
        return self.reviews.count()


class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ScriptureReference(models.Model):
    book = models.CharField(max_length=50)
    chapter = models.IntegerField()
    verse_start = models.IntegerField()
    verse_end = models.IntegerField(null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        if self.verse_end:
            return f"{self.book} {self.chapter}:{self.verse_start}-{self.verse_end}"
        return f"{self.book} {self.chapter}:{self.verse_start}"


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField()
    photo = models.ImageField(upload_to='author_photos/', blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class ChristianBook(models.Model):
    CATEGORY_CHOICES = (
        ('TH', 'Theology'),
        ('DV', 'Devotional'),
        ('BS', 'Bible Study'),
        ('CM', 'Christian Living'),
        ('AP', 'Apologetics'),
        ('BG', 'Biography'),
        ('CH', 'Church History'),
        ('FM', 'Family'),
        ('YT', 'Youth'),
        ('CH', 'Children'),
    )

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pages = models.IntegerField()
    publisher = models.CharField(max_length=200)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.bookreview_set.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0


class BookReview(models.Model):
    book = models.ForeignKey(ChristianBook, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['book', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.user.username} for {self.book.title}'


class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(ChristianBook)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s list: {self.name}"


class BibleStudyMaterial(models.Model):
    CATEGORY_CHOICES = [
        ('OLD_TESTAMENT', 'Old Testament'),
        ('NEW_TESTAMENT', 'New Testament'),
        ('THEOLOGY', 'Theology'),
        ('DISCIPLESHIP', 'Discipleship'),
        ('COMMENTARY', 'Commentary'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='bible_study_materials/')
    upload_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bible_studies'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='THEOLOGY'
    )

    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Bible Study Material'
        verbose_name_plural = 'Bible Study Materials'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('resources:bible_study_detail', args=[self.pk])

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('SERMON', 'Sermon'),
        ('STUDY', 'Bible Study'),
        ('ARTICLE', 'Article'),
        ('VIDEO', 'Video'),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    content = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resources/', null=True, blank=True)

    def __str__(self):
        return self.title


class DailyDevotion(models.Model):
    title = models.CharField(max_length=200)
    scripture_reference = models.CharField(max_length=100)
    scripture_text = models.TextField()
    devotional_content = models.TextField()
    prayer_focus = models.TextField()
    publication_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.publication_date}: {self.title}"

    class Meta:
        ordering = ['-publication_date']
        verbose_name = "Daily Devotion"
        verbose_name_plural = "Daily Devotions"


class Artist(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField()
    image = models.ImageField(upload_to='artists/')
    website = models.URLField(blank=True)
    social_media = models.JSONField(default=dict, blank=True)  # Store social media links

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='album_covers/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

    ordering = ['order']


class BibleStudy(models.Model):
    STUDY_TYPES = (
        ('OT', 'Old Testament'),
        ('NT', 'New Testament'),
        ('TH', 'Theology'),
        ('DC', 'Doctrine'),
        ('AP', 'Apologetics'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    study_type = models.CharField(max_length=2, choices=STUDY_TYPES)
    scripture_reference = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    materials = models.FileField(upload_to='bible_study_materials/', blank=True)
    video_link = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Bible Studies"

    def __str__(self):
        return self.title


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('TH', 'Theology'),
        ('BI', 'Biblical Studies'),
        ('DE', 'Devotional'),
        ('CH', 'Church History'),
        ('AP', 'Apologetics'),
        ('MI', 'Ministry'),
        ('DI', 'Discipleship'),
        ('PR', 'Prayer'),
        ('WO', 'Worship'),
        ('LE', 'Leadership'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='TH')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True)

    # Publication details
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, blank=True)

    # File attachments
    pdf_file = models.FileField(upload_to='book_files/', blank=True)
    sample_chapter = models.FileField(upload_to='book_samples/', blank=True)

    # Metadata
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('resources:book_detail', args=[self.pk])
