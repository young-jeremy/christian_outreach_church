from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User


class BibleCollegeProgram(models.Model):
    LEVEL_CHOICES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('doctorate', 'Doctorate')
    ]

    name = models.CharField(max_length=200, null=False, blank=False)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='certificate')
    description = models.TextField(null=False, blank=False)
    duration_years = models.PositiveIntegerField()
    credits_required = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bible College Program"
        verbose_name_plural = "Bible College Programs"

    def __str__(self):
        return f"{self.get_level_display()} in {self.name}"


class BibleCollegeCourse(models.Model):
    SEMESTER_CHOICES = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Summer')
    ]

    program = models.ForeignKey(BibleCollegeProgram, on_delete=models.CASCADE, related_name='bible_college_courses',
                                null=False, blank=False)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    credits = models.PositiveIntegerField()
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    year_level = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    syllabus = models.FileField(upload_to='bible_college/syllabi/', blank=True)

    class Meta:
        verbose_name = "Bible College Course"
        verbose_name_plural = "Bible College Courses"

    def __str__(self):
        return f"{self.code} - {self.title}"


class BibleCollegeStudent(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('leave', 'On Leave'),
        ('graduated', 'Graduated'),
        ('withdrawn', 'Withdrawn')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bible_college_student')
    program = models.ForeignKey(BibleCollegeProgram, on_delete=models.CASCADE, related_name='bible_college_students')
    enrollment_date = models.DateField()
    expected_graduation = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_year = models.PositiveIntegerField(null=True, blank=True)
    spiritual_reference = models.FileField(upload_to='bible_college/references/', blank=True)
    testimony = models.TextField()

    class Meta:
        verbose_name = "Bible College Student"
        verbose_name_plural = "Bible College Students"

    def __str__(self):
        return f"{self.user.username} - {self.program.name}"


class BibleCollegeEnrollment(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
        ('P', 'Pass'), ('I', 'Incomplete'), ('W', 'Withdrawn')
    ]

    student = models.ForeignKey(BibleCollegeStudent, on_delete=models.CASCADE, related_name='bible_college_enrollments')
    course = models.ForeignKey(BibleCollegeCourse, on_delete=models.CASCADE, related_name='bible_college_enrollments')
    semester = models.IntegerField(choices=BibleCollegeCourse.SEMESTER_CHOICES)
    year = models.PositiveIntegerField()
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Bible College Enrollment"
        verbose_name_plural = "Bible College Enrollments"
        unique_together = ['student', 'course', 'semester', 'year']

    def __str__(self):
        return f"{self.student.user.username} - {self.course.code}"


class BibleCollegeAssignment(models.Model):
    course = models.ForeignKey(BibleCollegeCourse, on_delete=models.CASCADE, related_name='bible_college_assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    total_marks = models.PositiveIntegerField()
    weight_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = "Bible College Assignment"
        verbose_name_plural = "Bible College Assignments"

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class BibleCollegeSubmission(models.Model):
    assignment = models.ForeignKey(BibleCollegeAssignment, on_delete=models.CASCADE,
                                   related_name='bible_college_submissions')
    student = models.ForeignKey(BibleCollegeStudent, on_delete=models.CASCADE, related_name='bible_college_submissions')
    submitted_file = models.FileField(upload_to='bible_college/assignments/')
    submission_date = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        verbose_name = "Bible College Submission"
        verbose_name_plural = "Bible College Submissions"
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"


class BibleCollegeFaculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bible_college_faculty')
    title = models.CharField(max_length=100)
    qualifications = models.TextField()
    bio = models.TextField()
    office_hours = models.TextField()
    courses = models.ManyToManyField(BibleCollegeCourse, related_name='bible_college_instructors')
    profile_image = models.ImageField(upload_to='bible_college/faculty/', blank=True)

    class Meta:
        verbose_name = "Bible College Faculty"
        verbose_name_plural = "Bible College Faculty Members"

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ChristianMentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ministry_focus = models.CharField(max_length=200)
    spiritual_journey = models.TextField()
    years_in_ministry = models.PositiveIntegerField()
    profile_image = models.ImageField(upload_to='christian_mentor_profiles/', null=True, blank=True)
    accepting_mentees = models.BooleanField(default=True)
    max_mentees = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.user.username} - {self.ministry_focus}"


class ChristianMentorshipSession(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    mentor = models.ForeignKey(ChristianMentorProfile, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    scripture_focus = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_participants = models.PositiveIntegerField(default=10)
    participants = models.ManyToManyField(User, related_name='christian_mentorship_sessions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    recording_url = models.URLField(blank=True, null=True)
    study_materials = models.FileField(upload_to='christian_mentorship_resources/', blank=True, null=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.topic} by {self.mentor.user.get_full_name()}"

    @property
    def is_full(self):
        return self.participants.count() >= self.max_participants


class ChristianMentorshipApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(ChristianMentorProfile, on_delete=models.CASCADE)
    spiritual_goals = models.TextField()
    faith_background = models.TextField()
    ministry_involvement = models.TextField()
    commitment_hours = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application from {self.applicant.username} to {self.mentor.user.username}"


class ChristianMentorshipFeedback(models.Model):
    session = models.ForeignKey(ChristianMentorshipSession, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    spiritual_growth_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    mentorship_quality = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField()
    prayer_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session', 'participant']

    def __str__(self):
        return f"Feedback for {self.session.topic} by {self.participant.username}"


class ChristianEducationLevel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Christian Education Level'
        verbose_name_plural = 'Christian Education Levels'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('education:education_level_detail', kwargs={'pk': self.pk})


class ChristianCourse(models.Model):
    CATEGORY_CHOICES = (
        ('bible_study', 'Bible Study'),
        ('theology', 'Theology'),
        ('apologetics', 'Apologetics'),
        ('ministry', 'Ministry'),
        ('discipleship', 'Discipleship'),
        ('leadership', 'Leadership'),
        ('missions', 'Missions'),
        ('ethics', 'Christian Ethics')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    level = models.ForeignKey(ChristianEducationLevel, on_delete=models.CASCADE, related_name='courses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    objectives = models.TextField()
    prerequisites = models.TextField(blank=True)
    duration_weeks = models.PositiveIntegerField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='christian_courses_teaching')
    image = models.ImageField(upload_to='christian_education/courses/', blank=True)
    syllabus = models.FileField(upload_to='christian_education/syllabi/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Christian Course'
        verbose_name_plural = 'Christian Courses'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('education:course_detail', kwargs={'slug': self.slug})


class ChristianModule(models.Model):
    course = models.ForeignKey(ChristianCourse, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    content = models.TextField()
    scripture_references = models.TextField()
    learning_activities = models.TextField()
    resources = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order', 'title']
        verbose_name = 'Christian Module'
        verbose_name_plural = 'Christian Modules'
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def get_absolute_url(self):
        return reverse('education:module_detail', kwargs={'course_slug': self.course.slug, 'pk': self.pk})


class ChristianAssignment(models.Model):
    TYPE_CHOICES = (
        ('quiz', 'Quiz'),
        ('essay', 'Essay'),
        ('project', 'Project'),
        ('presentation', 'Presentation'),
        ('discussion', 'Discussion')
    )

    module = models.ForeignKey(ChristianModule, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    assignment_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Assignment Type'
    )
    due_date = models.DateField(verbose_name='Due Date')
    points = models.PositiveIntegerField(verbose_name='Points')
    instructions = models.TextField(verbose_name='Instructions')
    rubric = models.TextField(blank=True, verbose_name='Rubric')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        ordering = ['module', 'due_date', 'title']
        verbose_name = 'Christian Assignment'
        verbose_name_plural = 'Christian Assignments'

    def __str__(self):
        return f"{self.module.title} - {self.title}"

    def get_absolute_url(self):
        return reverse('education:assignment_detail', kwargs={
            'course_slug': self.module.course.slug,
            'module_pk': self.module.pk,
            'pk': self.pk
        })


class ChristianAssignmentSubmission(models.Model):
    assignment = models.ForeignKey(ChristianAssignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='christian_assignment_submissions')
    content = models.TextField()
    file = models.FileField(upload_to='christian_education/submissions/', blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='christian_graded_submissions'
    )
    graded_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submission_date']
        verbose_name = 'Christian Assignment Submission'
        verbose_name_plural = 'Christian Assignment Submissions'
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assignment.title}"

    def get_absolute_url(self):
        return reverse('education:submission_detail', kwargs={'pk': self.pk})


class ChristianEnrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn')
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='christian_course_enrollments')
    course = models.ForeignKey(ChristianCourse, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-enrolled_date']
        verbose_name = 'Christian Enrollment'
        verbose_name_plural = 'Christian Enrollments'
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title}"

    def get_absolute_url(self):
        return reverse('education:enrollment_detail', kwargs={'pk': self.pk})


class ChristianDiscussion(models.Model):
    module = models.ForeignKey(ChristianModule, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Christian Discussion'
        verbose_name_plural = 'Christian Discussions'

    def __str__(self):
        return f"{self.module.title} - {self.title}"

    def get_absolute_url(self):
        return reverse('education:discussion_detail', kwargs={
            'course_slug': self.module.course.slug,
            'module_pk': self.module.pk,
            'pk': self.pk
        })


class ChristianDiscussionPost(models.Model):
    discussion = models.ForeignKey(ChristianDiscussion, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='christian_discussion_posts')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Christian Discussion Post'
        verbose_name_plural = 'Christian Discussion Posts'

    def __str__(self):
        return f"{self.author.get_full_name()} - {self.discussion.title}"

    def get_absolute_url(self):
        return reverse('education:post_detail', kwargs={'pk': self.pk})


class TheologicalCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Theological Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TheologicalResource(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('scholarly', 'Scholarly')
    )

    TYPE_CHOICES = (
        ('article', 'Article'),
        ('book', 'Book'),
        ('video', 'Video'),
        ('audio', 'Audio Sermon'),
        ('course', 'Course'),
        ('commentary', 'Commentary'),
        ('study_guide', 'Study Guide')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(TheologicalCategory, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField()
    content = models.TextField()
    scripture_references = models.TextField(help_text="Enter Bible references separated by commas")
    key_points = models.TextField()
    publication_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='theological/resources/', blank=True)
    external_link = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='theological/thumbnails/', blank=True)
    download_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    requires_permission = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class StudyNote(models.Model):
    resource = models.ForeignKey(TheologicalResource, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"


class ResourceReview(models.Model):
    resource = models.ForeignKey(TheologicalResource, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    theological_accuracy = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    clarity = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    practicality = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ['resource', 'user']

    def __str__(self):
        return f"Review by {self.user.get_full_name()} for {self.resource.title}"


class Bibliography(models.Model):
    resource = models.ForeignKey(TheologicalResource, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publication = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    pages = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'Bibliographies'

    def __str__(self):
        return f"{self.authors} - {self.title}"


class AgeGroup(models.Model):
    name = models.CharField(max_length=100)
    age_range = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.age_range})"


class SundaySchoolMaterial(models.Model):
    CATEGORY_CHOICES = (
        ('bible_story', 'Bible Story'),
        ('memory_verse', 'Memory Verse'),
        ('activity', 'Activity'),
        ('craft', 'Craft'),
        ('song', 'Song'),
        ('lesson', 'Full Lesson'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    bible_reference = models.CharField(max_length=100)
    main_points = models.TextField()
    learning_objectives = models.TextField()
    materials_needed = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    content = models.TextField()
    teacher_notes = models.TextField(blank=True)
    attachment = models.FileField(upload_to='sunday_school/materials/', blank=True)
    image = models.ImageField(upload_to='sunday_school/images/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Activity(models.Model):
    material = models.ForeignKey(SundaySchoolMaterial, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    materials_needed = models.TextField(blank=True)
    image = models.ImageField(upload_to='sunday_school/activities/', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.material.title} - {self.title}"


class TeachingResource(models.Model):
    RESOURCE_TYPES = (
        ('worksheet', 'Worksheet'),
        ('handout', 'Handout'),
        ('presentation', 'Presentation'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('game', 'Game'),
    )

    material = models.ForeignKey(SundaySchoolMaterial, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField()
    file = models.FileField(upload_to='sunday_school/resources/')
    is_downloadable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material.title} - {self.title}"


class Feedback(models.Model):
    material = models.ForeignKey(SundaySchoolMaterial, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    used_date = models.DateField()
    age_group_effectiveness = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    time_management = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    student_engagement = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    suggestions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.material.title} by {self.teacher.get_full_name()}"


class LeadershipTraining(models.Model):
    LEVEL_CHOICES = (
        ('basic', 'Basic Leadership'),
        ('intermediate', 'Intermediate Leadership'),
        ('advanced', 'Advanced Leadership'),
        ('mentor', 'Mentorship Training'),
    )

    CATEGORY_CHOICES = (
        ('pastoral', 'Pastoral Leadership'),
        ('ministry', 'Ministry Leadership'),
        ('youth', 'Youth Leadership'),
        ('worship', 'Worship Leadership'),
        ('admin', 'Administrative Leadership'),
        ('missions', 'Missions Leadership'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField()
    learning_objectives = models.TextField()
    prerequisites = models.TextField(blank=True)
    duration_weeks = models.PositiveIntegerField()
    max_participants = models.PositiveIntegerField()
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mentored_trainings')
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='leadership/courses/', blank=True)
    syllabus = models.FileField(upload_to='leadership/syllabi/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('leadership:training_detail', kwargs={'slug': self.slug})


class TrainingModule(models.Model):
    training = models.ForeignKey(LeadershipTraining, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    competencies = models.TextField()

    class Meta:
        ordering = ['order']
        unique_together = ['training', 'order']

    def __str__(self):
        return f"{self.training.title} - Module {self.order}: {self.title}"


class TrainingSession(models.Model):
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    practical_exercise = models.TextField()
    reflection_questions = models.TextField()
    resources = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'order']

    def __str__(self):
        return f"{self.module.training.title} - Session {self.order}: {self.title}"


class LeadershipAssessment(models.Model):
    ASSESSMENT_TYPES = (
        ('self', 'Self Assessment'),
        ('peer', 'Peer Review'),
        ('mentor', 'Mentor Evaluation'),
        ('practical', 'Practical Assessment'),
    )

    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    criteria = models.TextField()
    passing_score = models.PositiveIntegerField()
    due_days = models.PositiveIntegerField(help_text="Days to complete after session")

    def __str__(self):
        return f"{self.session.title} - {self.get_assessment_type_display()}"


class ParticipantEnrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
        ('on_hold', 'On Hold'),
    )

    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(LeadershipTraining, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_enrollments'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['participant', 'training']

    def __str__(self):
        return f"{self.participant.get_full_name()} - {self.training.title}"


class AssessmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('revision', 'Needs Revision'),
    )

    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(LeadershipAssessment, on_delete=models.CASCADE)
    submission_text = models.TextField()
    evidence_file = models.FileField(upload_to='leadership/submissions/', blank=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviewed_assessments'
    )
    reviewed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.participant.get_full_name()} - {self.assessment.title}"


class MentorshipSession(models.Model):
    training = models.ForeignKey(LeadershipTraining, on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentoring_sessions')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_sessions')
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    topics = models.TextField()
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Mentorship: {self.participant.get_full_name()} with {self.mentor.get_full_name()}"


class BiblicalCourse(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration_weeks = models.PositiveIntegerField()
    prerequisites = models.TextField(blank=True)
    image = models.ImageField(upload_to='courses/', blank=True)
    syllabus = models.FileField(upload_to='syllabi/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class StudentEnrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
        ('on_hold', 'On Hold'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(BiblicalCourse, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class CourseModule(models.Model):
    course = models.ForeignKey(BiblicalCourse, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    learning_objectives = models.TextField()

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    scripture_references = models.TextField()
    video_url = models.URLField(blank=True)
    audio_file = models.FileField(upload_to='lessons/audio/', blank=True)
    presentation = models.FileField(upload_to='lessons/presentations/', blank=True)
    additional_resources = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'order']

    def __str__(self):
        return f"{self.module.course.title} - Lesson {self.order}: {self.title}"


class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_days = models.PositiveIntegerField(help_text="Days to complete after lesson start")
    points = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class LessonProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'lesson']

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}"


class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('revision_needed', 'Revision Needed'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_text = models.TextField()
    file_upload = models.FileField(upload_to='assignments/submissions/', blank=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    grade = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='graded_assignments'
    )
    graded_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


class Discussion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Discussion replies'

    def __str__(self):
        return f"Reply to {self.discussion.title} by {self.created_by.username}"
