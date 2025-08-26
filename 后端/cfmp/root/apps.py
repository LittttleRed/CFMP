from django.apps import AppConfig


class Test123Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'root'

    def ready(self):
        from .schedulers import scheduler
        #scheduler.remove_all_jobs()
        #scheduler.start()
