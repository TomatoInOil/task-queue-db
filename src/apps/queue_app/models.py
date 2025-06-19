from django.db import models


class TaskQueue(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"

    task_name = models.CharField(
        max_length=255,
        verbose_name="Название задачи",
    )
    status = models.CharField(
        max_length=50,
        default=Status.PENDING,
        choices=Status.choices,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    def __str__(self):
        return self.task_name
