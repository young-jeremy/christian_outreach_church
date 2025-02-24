from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from accounts.models import User


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
