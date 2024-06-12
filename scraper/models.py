from django.db import models

# Create your models here.
import uuid

class ScrapeJob(models.Model):
    job_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')

class ScrapeTask(models.Model):
    job = models.ForeignKey(ScrapeJob, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=10)
    data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')
