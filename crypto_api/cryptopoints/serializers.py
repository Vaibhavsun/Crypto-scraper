from rest_framework import serializers
from .models import Jobs,Tasks
class job_serializer(serializers.Serializer):
    class Meta:
        model=Jobs
        fields=['job_id']
class task_serializer(serializers.Serializer):
    jobid=job_serializer()
    class Meta:
        model=Tasks
        fields='__all__'
