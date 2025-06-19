from rest_framework.views import Response, Request, status
from rest_framework.decorators import api_view


from apps.queue_app.serializers import TaskQueueSerializer
from apps.queue_app.service import fetch_task


@api_view(["PATCH"])
def fetch_task_view(request: Request):
    """
    Извлекает следующую доступную задачу из очереди и отмечает её как обрабатываемую.
    Если задача не найдена, возвращает 204 статус.
    """
    task = fetch_task()
    if task:
        serializer = TaskQueueSerializer(task)
        return Response(serializer.data)
    return Response(status=status.HTTP_204_NO_CONTENT)
