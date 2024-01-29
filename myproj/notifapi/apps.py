from django.apps import AppConfig


class NotifapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifapi'

    def ready(self):
        import notifapi.signals

