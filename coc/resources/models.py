from django.db import models
from accounts.models import User


class BibleStudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='bible_study_materials/')
    upload_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=[
        ('OLD_TESTAMENT', 'Old Testament'),
        ('NEW_TESTAMENT', 'New Testament'),
        ('THEOLOGY', 'Theology'),
        ('DISCIPLESHIP', 'Discipleship'),
        ('COMMENTARY', 'Commentary'),
    ])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']

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
