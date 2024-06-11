from django.db import models
import celery
class Jobs(models.Model):
    job_id=models.UUIDField(primary_key=True)
class Tasks(models.Model):
    jobid=models.OneToOneField(Jobs,on_delete=models.CASCADE,related_name='job')
    task=models.JSONField(default=list)
