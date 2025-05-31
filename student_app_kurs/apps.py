from django.apps import AppConfig

class student_app_kursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student_app_kurs'

    def ready(self):
        import student_app_kurs.signals  # импорт сигналов при запуске приложения
