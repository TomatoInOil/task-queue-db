from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.queue_app.models import TaskQueue


class FetchTaskViewTests(APITestCase):
    URL = reverse("fetch-task")
    TASK1_NAME = "Task 1"
    TASK2_NAME = "Task 2"
    PROCESSING_TASK_NAME = "Processing Task"
    NEW_TASK_NAME = "New Task"

    TASK_NAME_FIELD = "task_name"
    STATUS_FIELD = "status"

    def setUp(self):
        self.task1 = TaskQueue.objects.create(task_name=self.TASK1_NAME)
        self.task2 = TaskQueue.objects.create(task_name=self.TASK2_NAME)
        self.processing_task = TaskQueue.objects.create(
            task_name=self.PROCESSING_TASK_NAME, status=TaskQueue.Status.PROCESSING
        )

    def test_fetch_task_success(self):
        """Тест успешного получения задачи"""
        response = self.client.patch(self.URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[self.TASK_NAME_FIELD], self.TASK1_NAME)
        self.assertEqual(response.data[self.STATUS_FIELD], TaskQueue.Status.PROCESSING)
        task = TaskQueue.objects.get(id=self.task1.id)
        message_text = (
            "После извлечения задачи, статус должен был измениться на PROCESSING"
        )
        self.assertEqual(task.status, TaskQueue.Status.PROCESSING, msg=message_text)

    def test_fetch_task_no_available_tasks(self):
        """Тест получения ответа, когда нет доступных задач"""
        self.client.patch(self.URL)
        self.client.patch(self.URL)

        response = self.client.patch(self.URL)
        message_text = "Если нет доступных задач, то должен быть возвращен статус 204"
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, msg=message_text
        )

    def test_fetch_task_order(self):
        """Тест получения задач в порядке их создания"""
        response1 = self.client.patch(self.URL)
        self.assertEqual(response1.data[self.TASK_NAME_FIELD], self.TASK1_NAME)

        response2 = self.client.patch(self.URL)
        self.assertEqual(response2.data[self.TASK_NAME_FIELD], self.TASK2_NAME)

    def test_fetch_task_skip_processing(self):
        """Тест фильтрации задач"""
        TaskQueue.objects.create(task_name=self.NEW_TASK_NAME)

        response1 = self.client.patch(self.URL)
        self.assertEqual(response1.data[self.TASK_NAME_FIELD], self.TASK1_NAME)

        response2 = self.client.patch(self.URL)
        self.assertEqual(response2.data[self.TASK_NAME_FIELD], self.TASK2_NAME)

        response3 = self.client.patch(self.URL)
        message_text = (
            "Задача в статусе PROCESSING не должна быть извлечена. Ожидалась New Task"
        )
        self.assertEqual(
            response3.data[self.TASK_NAME_FIELD], self.NEW_TASK_NAME, msg=message_text
        )
