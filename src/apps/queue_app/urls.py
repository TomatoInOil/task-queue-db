from django.urls import path

from apps.queue_app.views import fetch_task_view

urlpatterns = [
    path("fetch-task/", fetch_task_view, name="fetch-task"),
]
