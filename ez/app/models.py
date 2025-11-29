from django.db import models

# Create your models here.
# app/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("normal", "Normal"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    source_type = models.CharField(max_length=20)  # text/file/url
    source_text = models.TextField(null=True, blank=True)
    source_file = models.FileField(upload_to="uploads/", null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)

    target_languages = models.JSONField()  # ["fr","hi"]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="normal")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
    progress = models.IntegerField(default=0)

    callback_url = models.URLField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    error_message = models.TextField(null=True, blank=True)
    attempt = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.status}"


class JobResult(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="result")
    result_data = models.JSONField()   # {"fr": "...", "hi": "..."}
    created_at = models.DateTimeField(auto_now_add=True)
