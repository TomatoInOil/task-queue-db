from django.apps import AppConfig


class QueueAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.queue_app"
    verbose_name = "Очередь задач"
