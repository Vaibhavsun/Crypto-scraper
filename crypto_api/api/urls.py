from cryptopoints.views import post_tasks
from django.urls import path

urlpatterns=[
    path('task/',post_tasks)
]