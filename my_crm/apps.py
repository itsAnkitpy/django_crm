from django.apps import AppConfig


class MyCrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_crm'

    def ready(self):
        import my_crm.signals 