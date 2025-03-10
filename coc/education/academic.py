from django.db import models


class BibleCollegeProgram(models.Model):
    LEVEL_CHOICES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('doctorate', 'Doctorate')
    ]

    name = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField()
    duration_years = models.PositiveIntegerField()
    credits_required = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"
        app_label = 'education'

    def __str__(self):
        return f"{self.get_level_display()} in {self.name}"


class BibleCollegeCourse(models.Model):
    SEMESTER_CHOICES = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Summer')
    ]

    program = models.ForeignKey('education.BibleCollegeProgram', on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.PositiveIntegerField()
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    year_level = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    syllabus = models.FileField(upload_to='bible_college/syllabi/', blank=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        app_label = 'education'

    def __str__(self):
        return f"{self.code} - {self.title}"


class BibleCollegeCourseEnrollment(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
        ('P', 'Pass'), ('I', 'Incomplete'), ('W', 'Withdrawn')
    ]

    student = models.ForeignKey('education.BibleCollegeStudent', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('education.BibleCollegeCourse', on_delete=models.CASCADE, related_name='enrollments')
    semester = models.IntegerField(choices=BibleCollegeCourse.SEMESTER_CHOICES)
    year = models.PositiveIntegerField()
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        app_label = 'education'
        unique_together = ['student', 'course', 'semester', 'year']

    def __str__(self):
        return f"{self.student.user.username} - {self.course.code}"
