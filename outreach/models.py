from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class EvangelismTool(models.Model):
    CATEGORY_CHOICES = [
        ('tract', 'Gospel Tract'),
        ('book', 'Book'),
        ('video', 'Video Resource'),
        ('audio', 'Audio Resource'),
        ('presentation', 'Presentation'),
        ('training', 'Training Material'),
        ('other', 'Other')
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('pt', 'Portuguese'),
        ('other', 'Other')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    file = models.FileField(upload_to='evangelism_tools/', blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='evangelism_tools/thumbnails/', blank=True, null=True)
    author = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    publication_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('outreach:tool_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    @property
    def resource_url(self):
        return self.external_link if self.external_link else self.file.url if self.file else None
