
from django.apps import AppConfig

# Define the DemoConfig class only once.

class DemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demo'

    def ready(self):
        # Ensure imports are within the ready method to avoid issues
        import demo.signals  # Place this here instead of top level


