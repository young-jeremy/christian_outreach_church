from django.db import models
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
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


class Mission(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    featured_image = models.ImageField(upload_to='missions/', blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    team_size = models.IntegerField(default=0)
    impact_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('outreach:mission_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('community', 'Community Development'),
        ('evangelism', 'Evangelism'),
        ('disaster', 'Disaster Relief'),
        ('youth', 'Youth Empowerment'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200)
    project_lead = models.CharField(max_length=100)
    contact_email = models.EmailField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    goals = models.TextField()
    outcomes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('outreach:project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='project_updates/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.project.title} - {self.title}"



class OutreachProgram(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
