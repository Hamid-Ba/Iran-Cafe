from django.apps import AppConfig

class ZarinpalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "zarinpal"

    def ready(self):
        import zarinpal.signals
