from django.apps import AppConfig


class StarsAppConfig(AppConfig):

    name = "starboard.stars"
    verbose_name = "Stars"

    def ready(self):
        try:
            import starboard.stars.signals  # noqa F401
        except ImportError:
            pass
