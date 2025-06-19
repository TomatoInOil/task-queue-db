from django.db import transaction

from apps.queue_app.models import TaskQueue


def fetch_task() -> TaskQueue | None:
    """Извлекает следующую доступную задачу из очереди."""
    with transaction.atomic():
        task = (
            TaskQueue.objects.select_for_update(skip_locked=True)
            .filter(status=TaskQueue.Status.PENDING)
            .order_by("created_at")
            .first()
        )
        if task:
            task.status = TaskQueue.Status.PROCESSING
            task.save()
            return task
    return None
