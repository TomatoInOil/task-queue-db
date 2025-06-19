from django.core.management.base import BaseCommand
from apps.queue_app.models import TaskQueue


class Command(BaseCommand):
    help = "Generate dummy tasks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Count of tasks to generate",
        )

    def handle(self, *args, **options):
        for _ in range(options["count"]):
            TaskQueue.objects.create(
                task_name=f"Task {_}",
                status=TaskQueue.Status.PENDING,
            )
