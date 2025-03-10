from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BibleCollegeStudent(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('leave', 'On Leave'),
        ('graduated', 'Graduated'),
        ('withdrawn', 'Withdrawn')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bible_college_student')
    program = models.ForeignKey('education.BibleCollegeProgram', on_delete=models.CASCADE, related_name='students')
    enrollment_date = models.DateField()
    expected_graduation = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_year = models.PositiveIntegerField()
    spiritual_reference = models.FileField(upload_to='bible_college/references/', blank=True)
    testimony = models.TextField()

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        app_label = 'education'

    def __str__(self):
        return f"{self.user.username} - {self.program.name}"


class BibleCollegeFaculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bible_college_faculty')
    title = models.CharField(max_length=100)
    qualifications = models.TextField()
    bio = models.TextField()
    office_hours = models.TextField()
    courses = models.ManyToManyField('education.BibleCollegeCourse', related_name='instructors')
    profile_image = models.ImageField(upload_to='bible_college/faculty/', blank=True)

    class Meta:
        verbose_name = "Faculty Member"
        verbose_name_plural = "Faculty Members"
        app_label = 'education'

    def __str__(self):
        return f"{self.user.username} - {self.title}"
