from django.apps import AppConfig



class AuthApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_api"

    def ready(self):
        """Runs once when Django finishes initializing."""
        from helper.server_scheduler import start_scheduler
        try:
            start_scheduler()
        except Exception as e:
            from helper.logger import onion
            onion("keep_alive", f"Failed to start scheduler: {str(e)}")
