from django.apps import AppConfig

class AsztroappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asztroapp'

    def ready(self):
        import asztroapp.signals  # ha van ilyen modulod
