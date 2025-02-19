from django.db import models


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
