from django.contrib import admin

from .models import TaskQueue


@admin.register(TaskQueue)
class TaskQueueAdmin(admin.ModelAdmin):
    list_display = ("task_name", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("task_name",)
