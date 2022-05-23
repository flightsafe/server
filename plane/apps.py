from django.apps import AppConfig


class PlaneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plane'

    def ready(self):
        import plane.signals
        print(f"using signals {plane.signals}")
