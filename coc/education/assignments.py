from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class BibleCollegeAssignment(models.Model):
    course = models.ForeignKey('education.BibleCollegeCourse', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    total_marks = models.PositiveIntegerField()
    weight_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        app_label = 'education'

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class BibleCollegeAssignmentSubmission(models.Model):
    assignment = models.ForeignKey('education.BibleCollegeAssignment', on_delete=models.CASCADE,
                                   related_name='submissions')
    student = models.ForeignKey('education.BibleCollegeStudent', on_delete=models.CASCADE, related_name='submissions')
    submitted_file = models.FileField(upload_to='bible_college/assignments/')
    submission_date = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        verbose_name = "Assignment Submission"
        verbose_name_plural = "Assignment Submissions"
        app_label = 'education'
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"
