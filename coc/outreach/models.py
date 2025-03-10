from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    visiting_hours = models.TextField()
    special_instructions = models.TextField(help_text="Special requirements or protocols")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    floor = models.CharField(max_length=50)
    visiting_restrictions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class MinistryService(models.Model):
    SERVICE_TYPES = (
        ('prayer', 'Prayer Support'),
        ('communion', 'Holy Communion'),
        ('counseling', 'Spiritual Counseling'),
        ('worship', 'Worship Service'),
        ('visitation', 'General Visitation'),
        ('support_group', 'Support Group'),
    )

    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    max_participants = models.PositiveIntegerField()
    materials_needed = models.TextField(blank=True)
    departments = models.ManyToManyField(Department)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_service_type_display()})"


class VisitSchedule(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    service = models.ForeignKey(MinistryService, on_delete=models.CASCADE)
    date = models.DateTimeField()
    volunteers = models.ManyToManyField(User, related_name='hospital_visits')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.title} at {self.hospital.name} - {self.date}"


class PatientRequest(models.Model):
    PRIORITY_CHOICES = (
        ('urgent', 'Urgent'),
        ('normal', 'Normal'),
        ('scheduled', 'Scheduled'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    service_requested = models.ForeignKey(MinistryService, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    special_notes = models.TextField(blank=True)
    preferred_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request for {self.patient_name} - {self.service_requested.title}"


class HospitalVolunteer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('inactive', 'Inactive'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospitals = models.ManyToManyField(Hospital)
    services = models.ManyToManyField(MinistryService)
    availability = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    medical_training = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    orientation_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Hospital Volunteer"


class PrisonFacility(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    visiting_hours = models.TextField()
    requirements = models.TextField(help_text="Entry requirements and regulations")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Prison Facilities"

    def __str__(self):
        return self.name


class InmateProgram(models.Model):
    PROGRAM_TYPES = (
        ('bible_study', 'Bible Study'),
        ('counseling', 'Counseling'),
        ('worship', 'Worship Service'),
        ('discipleship', 'Discipleship'),
        ('life_skills', 'Life Skills'),
        ('reentry', 'Re-entry Program'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    facility = models.ForeignKey(PrisonFacility, on_delete=models.CASCADE)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    description = models.TextField()
    schedule = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField()
    volunteers_needed = models.PositiveIntegerField()
    materials_needed = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.facility.name}"


class PrisonVisit(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    facility = models.ForeignKey(PrisonFacility, on_delete=models.CASCADE)
    program = models.ForeignKey(InmateProgram, on_delete=models.CASCADE)
    date = models.DateTimeField()
    volunteers = models.ManyToManyField(User, related_name='prison_visits')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    attendance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.program.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"


class VolunteerApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facility = models.ForeignKey(PrisonFacility, on_delete=models.CASCADE)
    programs = models.ManyToManyField(InmateProgram)
    experience = models.TextField()
    motivation = models.TextField()
    availability = models.TextField()
    references = models.TextField()
    background_check_consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewer_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.facility.name}"


class MinistryResource(models.Model):
    RESOURCE_TYPES = (
        ('book', 'Book'),
        ('bible', 'Bible'),
        ('study_material', 'Study Material'),
        ('video', 'Video'),
        ('music', 'Music'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    facility = models.ForeignKey(PrisonFacility, on_delete=models.CASCADE)
    program = models.ForeignKey(InmateProgram, on_delete=models.CASCADE, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"


class PrisonVisitReport(models.Model):
    title = models.CharField(max_length=200)  # Add this field
    visit = models.OneToOneField('PrisonVisit', on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    inmates_attended = models.PositiveIntegerField()
    activities_conducted = models.TextField()
    prayer_requests = models.TextField(blank=True)
    testimonies = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    follow_up_needed = models.TextField(blank=True)
    resources_used = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Prison Visit Report'
        verbose_name_plural = 'Prison Visit Reports'

    def __str__(self):
        return f"Report for {self.visit} - {self.date.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Visit Report - {self.visit.program.title} - {self.date.strftime('%Y-%m-%d')}"
        super().save(*args, **kwargs)


class DiscipleshipTrack(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration_weeks = models.PositiveIntegerField(help_text="Duration in weeks")
    prerequisites = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='discipleship/%Y/%m/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['level', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class DiscipleshipModule(models.Model):
    track = models.ForeignKey(DiscipleshipTrack, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    learning_objectives = models.TextField()
    estimated_hours = models.PositiveIntegerField(help_text="Estimated hours to complete")

    class Meta:
        ordering = ['track', 'order']
        unique_together = ['track', 'order']

    def __str__(self):
        return f"{self.track.title} - Module {self.order}: {self.title}"


class DiscipleshipLesson(models.Model):
    module = models.ForeignKey(DiscipleshipModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    scripture_references = models.TextField()
    reflection_questions = models.TextField()
    order = models.PositiveIntegerField()
    video_url = models.URLField(blank=True)
    additional_resources = models.TextField(blank=True)

    class Meta:
        ordering = ['module', 'order']
        unique_together = ['module', 'order']

    def __str__(self):
        return f"{self.module.title} - Lesson {self.order}: {self.title}"


class MentorshipRelationship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated')
    )

    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentoring')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='being_mentored')
    track = models.ForeignKey(DiscipleshipTrack, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    goals = models.TextField()
    meeting_frequency = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['mentor', 'mentee', 'track']

    def __str__(self):
        return f"{self.mentor.username} mentoring {self.mentee.username} - {self.track.title}"


class DiscipleshipProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discipleship_progress')
    lesson = models.ForeignKey(DiscipleshipLesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    reflection = models.TextField(blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class MentorshipMeeting(models.Model):
    relationship = models.ForeignKey(MentorshipRelationship, on_delete=models.CASCADE, related_name='meetings')
    date = models.DateTimeField()
    topics_discussed = models.TextField()
    action_items = models.TextField()
    next_meeting_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meeting between {self.relationship.mentor.username} and {self.relationship.mentee.username} on {self.date}"


class CharityCampaign(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    cause = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(upload_to='charity_campaigns/%Y/%m/%d/', blank=True)
    beneficiary = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Charity Campaigns"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_progress_percentage(self):
        if self.target_amount > 0:
            return int((self.raised_amount / self.target_amount) * 100)
        return 0


class Donation(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    )

    campaign = models.ForeignKey(CharityCampaign, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of ${self.amount} by {self.donor.username if self.donor else 'Anonymous'}"


class CharityEvent(models.Model):
    campaign = models.ForeignKey(CharityCampaign, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField()
    current_participants = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(CharityEvent, on_delete=models.CASCADE, related_name='registrations')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='charity_events')
    registration_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ['event', 'participant']

    def __str__(self):
        return f"{self.participant.username} - {self.event.title}"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class", default="fas fa-hands-helping")

    class Meta:
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class ServiceProject(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField()
    location = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    volunteers_needed = models.PositiveIntegerField()
    skills_required = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='service_projects/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ServiceHours(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_hours')
    project = models.ForeignKey(ServiceProject, on_delete=models.CASCADE, related_name='volunteer_hours')
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=1)
    description = models.TextField()
    verified_by = models.CharField(max_length=100, blank=True)
    verification_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service Hours"
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.username} - {self.project.title} ({self.hours} hours)"


class ServiceReflection(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_reflections')
    project = models.ForeignKey(ServiceProject, on_delete=models.CASCADE, related_name='reflections')
    reflection = models.TextField()
    impact = models.TextField(help_text="Describe the impact of your service on the community")
    learning = models.TextField(help_text="What did you learn from this experience?")
    images = models.ImageField(upload_to='service_reflections/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reflection by {self.student.username} on {self.project.title}"



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


class HospitalVisitReport(models.Model):
    title = models.CharField(max_length=200)
    visit = models.OneToOneField(VisitSchedule, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    patients_visited = models.PositiveIntegerField()
    prayer_requests = models.TextField(blank=True)
    testimonies = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    follow_up_needed = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Hospital Visit Report'
        verbose_name_plural = 'Hospital Visit Reports'

    def __str__(self):
        return f"Report for {self.visit} - {self.date.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Visit Report - {self.visit.service.title} - {self.date.strftime('%Y-%m-%d')}"
        super().save(*args, **kwargs)
