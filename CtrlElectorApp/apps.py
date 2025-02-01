from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CtrlElectorApp'

    def ready(self):
        import CtrlElectorApp.signals

